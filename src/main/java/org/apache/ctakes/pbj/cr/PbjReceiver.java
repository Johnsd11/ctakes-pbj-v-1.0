package org.apache.ctakes.pbj.cr;

import org.apache.activemq.artemis.jms.client.ActiveMQBytesMessage;
import org.apache.activemq.artemis.jms.client.ActiveMQConnectionFactory;
import org.apache.activemq.artemis.jms.client.ActiveMQQueue;
import org.apache.ctakes.core.cc.pretty.plaintext.PrettyTextWriterFit;
import org.apache.ctakes.core.config.ConfigParameterConstants;
import org.apache.ctakes.core.pipeline.PipeBitInfo;
import org.apache.ctakes.core.pipeline.PipelineBuilder;
import org.apache.ctakes.core.util.doc.JCasBuilder;
import org.apache.log4j.Logger;
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
import java.io.BufferedInputStream;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;

import static org.apache.ctakes.pbj.PbjUtil.*;



@PipeBitInfo(
      name = "PbjReceiver",
      description = "Populates JCas based upon XMI content read from an Artemis Queue.",
      role = PipeBitInfo.Role.SPECIAL
)

public class PbjReceiver extends JCasCollectionReader_ImplBase {

   // to add a configuration parameter, type "param" and hit tab.
   static public final String PARAM_RECEIVER_NAME = "ReceiverName";
   static public final String PARAM_RECEIVER_PASS = "ReceiverPass";
   static public final String PARAM_HOST = "ReceiveHost";
   static public final String PARAM_PORT = "ReceivePort";
   static public final String PARAM_QUEUE = "ReceiveQueue";
   static public final String PARAM_ACCEPT_STOP = "AcceptStop";

   static public final String DESC_RECEIVER_NAME = "Your Artemis Username.";
   static public final String DESC_RECEIVER_PASS = "Your Artemis Password.";
   static public final String DESC_HOST = "The Artemis Host from which to receive information.";
   static public final String DESC_PORT = "The Artemis Port from which to receive information.";
   static public final String DESC_QUEUE = "The Artemis Queue from which to receive information.";
   static public final String DESC_ACCEPT_STOP = "Yes to shut down when the sender sends a stop signal.";

   static private final Logger LOGGER = Logger.getLogger( "PbjReceiver" );
   static private final String EMPTY_CAS = "BadMessageFormatReceivedCreateEmptyJCas";

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
         description = DESC_ACCEPT_STOP,
         mandatory = false,
         defaultValue = DEFAULT_ACCEPT_STOP
   )
   private String _acceptStop;

   private MessageConsumer _consumer;
   //private boolean _stop = false;
   private int _casCount = 0;
   private String _messageText = "";


   /**
    * {@inheritDoc}
    */
   @Override
   public void initialize( final UimaContext context ) throws ResourceInitializationException {
      super.initialize( context );
      consume();
   }

   /**
    * Creates and starts ActiveMQ connection which uses the configuration provided by user.
    *
    * @throws ResourceInitializationException -
    */
   private void consume() throws ResourceInitializationException{
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
         final ActiveMQQueue queue = new ActiveMQQueue( _queueName );
         _consumer = session.createConsumer( queue );
         connection.start();
         LOGGER.info( "Python Bridging Java Receiver Started on " + _hostName + " " + _queueName );
      } catch ( NamingException | JMSException IO ) {
         throw new ResourceInitializationException(IO);
      }
   }

   /**
    * Will continue to get more text until it reaches 'DISCONNECT_ME' (STOP SIGNAL)
    * {@inheritDoc} - Does the same thing as it's parent
    */
   @Override
   public void getNext( final JCas jCas ) throws IOException, CollectionException {
      if ( _messageText.equals( EMPTY_CAS ) ) {
         new JCasBuilder().setDocText( "" )
                          .rebuild( jCas );
         return;
      }
      try ( InputStream textStream = new BufferedInputStream( new ByteArrayInputStream( _messageText.getBytes() ) ) ) {
         XmiCasDeserializer.deserialize( textStream, jCas.getCas() );
         _casCount++;
      } catch ( SAXException e ) {
         throw new CollectionException( e );
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
    * {@inheritDoc}
    */
   @Override
   public boolean hasNext() throws CollectionException {
      try {
         final Message message = _consumer.receive();
         String text = "";
         if ( message instanceof TextMessage ) {
            text = ( (TextMessage) message ).getText();
         } else if ( message instanceof ActiveMQBytesMessage ) {
            text = readBytesMessage( (BytesMessage) message );
         } else if ( message != null ) {
            LOGGER.error( "Received unexpected message format " + message.getClass()
                                                                         .getName()
                          + "\n" + message.toString() + "\nProcessing Empty Document." );
            text = EMPTY_CAS;
         }
         //println( "Testing this right now :" + text );
         if ( !text.isEmpty() ) {
            if ( _acceptStop.equalsIgnoreCase( "yes" ) && text.equals( STOP_MESSAGE ) ) {
               return false;
            }
            _messageText = text;
         }
      } catch ( JMSException jmsE ) {
         throw new CollectionException( jmsE );
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


   /**
    * Start a PbjReceiver, listening to a queue named "testQueue" and accepting a stop signal sent from any PbjSender.
    * Writes Marked up plaintext files to a directory named "output" in the current working directory.
    *
    * @param args -
    */
   public static void main( String[] args ) {
      try {
         new PipelineBuilder().set( PARAM_ACCEPT_STOP, "yes" )
                              .set( PARAM_QUEUE, "testQueue" )
                              .reader( PbjReceiver.class )
                              .set( ConfigParameterConstants.PARAM_OUTPUTDIR, "output" )
                              .add( PrettyTextWriterFit.class )
                              .run();
      } catch ( UIMAException | IOException IO ) {
         System.err.println( IO.getMessage() );
      }

      // Below is the equivalent instruction set for a piper file:

      // set ACCEPT_REMOTE_STOP=yes
      // set RECEIVE_QUEUE=testQueue
      // reader PbjReceiver
      // set OutputDirectory=output
      // add pretty.plaintext.PrettyTextWriterFit
   }


}
