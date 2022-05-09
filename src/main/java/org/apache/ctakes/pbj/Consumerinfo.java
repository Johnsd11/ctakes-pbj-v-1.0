package org.apache.ctakes.pbj;

import org.apache.activemq.ActiveMQConnectionFactory;
import org.apache.activemq.broker.BrokerFactory;
import org.apache.activemq.broker.BrokerService;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.resource.ResourceInitializationException;

import javax.jms.Connection;
import javax.jms.ConnectionFactory;
import javax.jms.JMSException;
import javax.jms.Session;
import java.net.URI;

/**
 * @author DJ , chip-nlp
 * @since {1/13/22}
 */
public enum Consumerinfo {
   INSTANCE;



   static public Consumerinfo getInstance() {
      return INSTANCE;
   }

   static public final String DEFAULT_HOST = "localhost";
   static public final int DEFAULT_PORT = 61616;

   static private final Object LOCK = new Object();
   private String _host = DEFAULT_HOST;
   private int _port = DEFAULT_PORT;
   private Session _session;
   private boolean _brokerStarted = false;

   public void setHost( final String host ) {
      _host = host;
   }

   public String getHost() {
      return _host;
   }

   public void setPort( final int port ) {
      _port = port;
   }

   public int getPort() {
      return _port;
   }


   public void startBroker() throws ResourceInitializationException {
      synchronized ( LOCK ) {
         if ( _brokerStarted ) {
            return;
         }
         try {
            final BrokerService broker
                  = BrokerFactory.createBroker( new URI( "broker:(tcp://" + _host + ":" + _port + ")" ) );
            broker.start();
            _brokerStarted = true;
         } catch ( Exception e ) {
            throw new ResourceInitializationException( e );
         }
      }
   }


   public Session createSession() throws ResourceInitializationException {
      synchronized ( LOCK ) {
         if ( _session != null ) {
            return _session;
         }
         try {
            final ConnectionFactory connectionFactory
                  = new ActiveMQConnectionFactory( "tcp://" + _host + ":" + _port );
            final Connection connection = connectionFactory.createConnection();
            connection.start();
            _session = connection.createSession( false, Session.AUTO_ACKNOWLEDGE );
         } catch ( JMSException jmsE ) {
            throw new ResourceInitializationException( jmsE );
         }
         return _session;
      }
   }

   public Session getSession() {
      return _session;
   }

   public void disconnect() throws AnalysisEngineProcessException {
      synchronized ( LOCK ) {
         if ( _session == null ) {
            return;
         }
         try {
            _session.close();
            _session = null;
         } catch ( JMSException jmsE ) {
            throw new AnalysisEngineProcessException( jmsE );
         }
      }
   }


}
