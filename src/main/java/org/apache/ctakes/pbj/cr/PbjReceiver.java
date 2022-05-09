package org.apache.ctakes.pbj.cr;

import org.apache.activemq.artemis.jms.client.ActiveMQBytesMessage;
import org.apache.activemq.artemis.jms.client.ActiveMQConnectionFactory;
import org.apache.activemq.artemis.jms.client.ActiveMQQueue;
import org.apache.ctakes.core.cc.pretty.plaintext.PrettyTextWriterFit;
import org.apache.ctakes.core.pipeline.PipeBitInfo;
import org.apache.ctakes.core.pipeline.PipelineBuilder;
//import org.apache.ctakes.pbj.process.wrapper.JCasProcessor;
import org.apache.ctakes.typesystem.type.textsem.AnatomicalSiteMention;
import org.apache.uima.UIMAException;
import org.apache.uima.UimaContext;
import org.apache.uima.cas.impl.XmiCasDeserializer;
import org.apache.uima.collection.CollectionException;
import org.apache.uima.fit.component.JCasCollectionReader_ImplBase;
import org.apache.uima.fit.descriptor.ConfigurationParameter;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;
import org.apache.uima.util.Progress;
import org.apache.uima.util.ProgressImpl;
import org.xml.sax.SAXException;

import javax.jms.*;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import java.io.*;

import static org.apache.ctakes.pbj.PbjUtil.*;


/**
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */


//import org.apache.uima.jcas.tcas.DocumentAnnotation;

/**
 *
 * The original code was copied from org.apache.uima.examples.cpe.FileSystemCollectionReader
 * and modified for Mayo use.
 *
 * This collection reader facilitates reading "documents" from a single file.  Each
 * line in the document will be considered an entity to be analyzed by the CPE.  That
 * is each line will be treated as a "document" and will have its own CAS.
 *
 * Extremely large files will require large memory resources as each line is read into
 * memory upon initialization.  This was done to simplify implementation.
 *
 * @author Philip V. Ogren
 *
 */


@PipeBitInfo(
      name = "PbjReceiver",
      description = "Populates JCas based upon XMI content read from an Artemis Queue.",
      role = PipeBitInfo.Role.READER,
      products = { PipeBitInfo.TypeProduct.DOCUMENT_ID }
)

public class PbjReceiver extends JCasCollectionReader_ImplBase {

   // to add a configuration parameter, type "param" and hit tab.
   static public final String PARAM_RECEIVER_NAME = "RECEIVER_NAME";
   static public final String PARAM_RECEIVER_PASS = "RECEIVER_PASS";
   static private final String PARAM_ACCEPT_STOP = "DISCONNECT_ME";
   static public final String PARAM_HOST = "HOST";
   static public final String PARAM_PORT = "PORT";
   static public final String PARAM_QUEUE = "QUEUE";

   static public final String DESC_RECEIVER_NAME = "Set a value for Username";
   static public final String DESC_RECEIVER_PASS = "Set a value for Password";
   static public final String DESC_HOST = "Set a value for Host";
   static public final String DESC_PORT = "Set a value for Port";
   static public final String DESC_QUEUE = "Set a value for Queue";
   static public final String DESC_DISC = "Set a value for Disconnect";



   @ConfigurationParameter(
           name = PARAM_RECEIVER_NAME,
           description = DESC_RECEIVER_NAME,
           mandatory = false,
           defaultValue = DEFAULT_USER
   )
   private String _userName;

   @ConfigurationParameter(
           name = PARAM_RECEIVER_PASS,
           description = DESC_RECEIVER_PASS,
           mandatory = false,
           defaultValue = DEFAULT_PASS
   )
   private String _password;


   @ConfigurationParameter(
         name = PARAM_HOST,
         description = DESC_HOST,
         mandatory = false,
         defaultValue = DEFAULT_HOST
   )
   private String _hostName;

   @ConfigurationParameter(
         name = PARAM_PORT,
         description = DESC_PORT,
         mandatory = false
   )
   private int _port = DEFAULT_PORT;

   @ConfigurationParameter(
         name = PARAM_QUEUE,
         description = DESC_QUEUE
   )
   private String _queueName;

   @ConfigurationParameter(
         name = PARAM_ACCEPT_STOP,
         description = DESC_DISC,
         mandatory = false,
           defaultValue = DEFAULT_ACCEPT_STOP
   )
   private String _acceptStop;

   private MessageConsumer _consumer;
   //private boolean _stop = false;
   private int _casCount = 0;
   private String _messageText = "";


   /**
    *
    * {@inheritDoc}
    */
   @Override
   public void initialize( UimaContext context ) throws ResourceInitializationException {
      super.initialize(context);
      consume();
   }

   /**
    * Creates and starts ActiveMQ connection which uses HostName and Port provided by user.
    *
    * @throws ResourceInitializationException
    */
   private void consume() throws ResourceInitializationException{
      boolean complete = false;
      Connection connection = null;
      InitialContext context = null;
      try {
         context = new InitialContext();
         final ActiveMQConnectionFactory cf = new ActiveMQConnectionFactory( "tcp://" + _hostName + ":" + _port);
         // Time To Live TTL of -1 asks server to never close this connection.
         cf.setConnectionTTL( -1 );
         cf.setReconnectAttempts( -1 );
         // On the java side we don't need to parse STOMP.  JMS will automatically translate.
         connection = cf.createConnection();
         final Session session = connection.createSession( false, Session.AUTO_ACKNOWLEDGE );
         final ActiveMQQueue queue = new ActiveMQQueue(_queueName);
         _consumer = session.createConsumer( queue );
         connection.start();
         System.out.println( "New Consumer Started!" );
      } catch ( NamingException | JMSException IO ) {
         throw new ResourceInitializationException(IO);
      }
   }

   /**
    * Will continue to get more text until it reaches 'DISCONNECT_ME' (STOP SIGNAL)
    * {@inheritDoc} - Does the same thing as it's parent
    */
   @Override
   public void getNext( final JCas cas ) throws IOException, CollectionException {
      try( InputStream textStream = new BufferedInputStream( new ByteArrayInputStream(_messageText.getBytes() ) ) ) {
         XmiCasDeserializer.deserialize( textStream, cas.getCas() );
         _casCount++;
      } catch (SAXException e) {
         throw new CollectionException(e);
      }
   }

   /**
    * @param message BytesMessage to consume.  Using the content-type text/plain produces a message with a byte array.
    * @return text from bytes.
    * @throws JMSException -
    */
   static private String readBytesMessage( final BytesMessage message ) throws JMSException {
      final StringBuilder sb = new StringBuilder();
      byte[] buffer = new byte[1024];
      int size = message.readBytes( buffer );
      while ( size > 0 ) {
         sb.append( new String( buffer, 0, size ) );
         size = message.readBytes( buffer );
      }
      return sb.toString();
   }


   /**
    *
    * {@inheritDoc}
    */
   @Override
   public boolean hasNext() throws IOException, CollectionException {
      try{
         final Message message = _consumer.receive();
         String text = "";
         if ( message instanceof TextMessage ) {
            text = ((TextMessage)message).getText();
         } else if ( message instanceof ActiveMQBytesMessage ) {
            text = readBytesMessage( (BytesMessage) message );
         } else if ( message != null ){
            throw new CollectionException(new IOException("Got unexpected message " + message.getClass().getName() +
                                                          "\n" + message.toString()));
         }
         //println( "Testing this right now :" + text );
         if ( !text.isEmpty() ) {
            if ( _acceptStop.equals( "yes" ) && text.equals( STOP_MESSAGE )) {
               return false;
            }
            _messageText = text;
         }
      }
      catch ( JMSException Io ){
         throw new CollectionException(Io);
      }
      return true;
   }

   /**
    *
    * {@inheritDoc}
    */
   @Override
   public Progress[] getProgress() {
      return new Progress[]{
            new ProgressImpl( _casCount, Integer.MAX_VALUE, Progress.ENTITIES )
      };
   }


   public void setQueue( String queue){
      _queueName = queue;
   }

   public void setHost( String host){
      _hostName = host;
   }

   public void setPort( int port){
      _port = port;
   }

//   public void setJCasProcessor(JCasProcessor processor){
//      // ctakes uses an uima pipeline, so the cas processor is essentially the rest of the pipeline.
//   }

   public void receiveJCas(){
      // since this is actually an uima collection reader, getNext() handles jcas reception.
   }

   public void handleJCas(){

   }

   public void setUserName( final String userName){
      _userName = userName;
   }

   public void setPassword( final String password){
      _password = password;
   }


   public static void main( String[] args ) {
      try {
         //println(  );
         new PipelineBuilder().set( PARAM_ACCEPT_STOP, "yes" )
                              .set( PARAM_QUEUE, "testQueue" )
                              .reader( PbjReceiver.class )
                              .set( "OutputDirectory", "/Users/CHIPadmin/Desktop" )
                              .add( PrettyTextWriterFit.class )
                              .run( );
                              //.add( HtmlTextWriter.class)
                              //.add( PropertyTextWriterFit.class )

      }
      //This is what would be in a piper file
      //set DISCONNECT_ME=yes
      //set QUEUE=testQueue
      //reader Consumer
      //set OutputDirectory=/Users/CHIPadmin/Desktop
      //add pretty.html.HtmlTextWriter
      //add pretty.plaintext.PrettyTextWriterFit
      //add property.plaintext.PropertyTextWriterFit

      catch( UIMAException | IOException IO) {
         System.err.println(IO.getMessage());
      }
   }


}
