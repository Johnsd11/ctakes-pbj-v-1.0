package org.apache.ctakes.pbj.ae;

import org.apache.ctakes.core.pipeline.PipeBitInfo;
import org.apache.ctakes.core.util.external.SystemUtil;
import org.apache.ctakes.core.util.log.DotLogger;
import org.apache.log4j.Logger;
import org.apache.uima.UimaContext;
import org.apache.uima.analysis_engine.AnalysisEngineDescription;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.fit.component.JCasAnnotator_ImplBase;
import org.apache.uima.fit.descriptor.ConfigurationParameter;
import org.apache.uima.fit.factory.AnalysisEngineFactory;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;

import java.io.File;
import java.io.IOException;

/**
 * @author SPF , chip-nlp
 * @since {5/10/2022}
 */
@PipeBitInfo(
      name = "ArtemisStarter",
      description = "Starts an Apache Artemis broker.",
      role = PipeBitInfo.Role.SPECIAL
)
public class ArtemisStarter extends ArtemisController {

   static private final Logger LOGGER = Logger.getLogger( "ArtemisStarter" );



   /**
    * {@inheritDoc}
    */
   @Override
   public void initialize( final UimaContext context ) throws ResourceInitializationException {
      super.initialize( context );
      if (LOG_FILE_DEFAULT.equals(_logFile)){
         _logFile = "ctakes_artemis_starter.log";
      }
      if ( _artemisRoot != null && !_artemisRoot.isEmpty() && !( new File( _artemisRoot ).exists() ) ) {
         LOGGER.warn( "Cannot find Artemis Root Directory " + _artemisRoot );
      }
      try {
         runCommand();
      } catch ( IOException ioE ) {
         throw new ResourceInitializationException( ioE );
      }
   }
   /**
    * {@inheritDoc}
    */
   @Override
   public void process( final JCas jcas ) throws AnalysisEngineProcessException {
      // Implementation of the process(..) method is mandatory, even if it does nothing.
   }

   private void runCommand() throws IOException {
      final SystemUtil.CommandRunner runner
            = new SystemUtil.CommandRunner( "bin" + File.separatorChar + "artemis run" );
      runner.setLogFiles( _logFile, _logFile );
      if ( _artemisRoot != null && !_artemisRoot.isEmpty() ) {
         runner.setDirectory( _artemisRoot );
      }
      LOGGER.info( "Starting Apache Artemis ..." );
      SystemUtil.run( runner );
      if ( _pause < 1 ) {
         return;
      }
      final long pause = _pause * 1000L;
      LOGGER.info( "Pausing " + _pause + " seconds ..." );
      try ( DotLogger dotter = new DotLogger() ) {
         Thread.sleep( pause );
      } catch ( IOException | InterruptedException multE ) {
         // do nothing
      }
   }

   static public AnalysisEngineDescription createEngineDescription( final String artemisDir )
         throws ResourceInitializationException {
      return AnalysisEngineFactory.createEngineDescription( ArtemisStarter.class, ArtemisStarter.DIR_PARAM, artemisDir );
   }


}
