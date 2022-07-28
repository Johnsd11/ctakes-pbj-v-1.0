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
        name = "ArtemisStopper",
        description = "Starts an Apache Artemis broker.",
        role = PipeBitInfo.Role.SPECIAL
)
public class ArtemisStopper extends JCasAnnotator_ImplBase {

    static private final Logger LOGGER = Logger.getLogger( "ArtemisStopper" );


    static public final String DIR_PARAM = "ArtemisRoot";
    static public final String DIR_DESC = "Your Artemis root directory.";
    @ConfigurationParameter(
            name = DIR_PARAM,
            description = DIR_DESC,
            mandatory = false
    )
    private String _artemisRoot;


    static public final String LOG_FILE_PARAM = "ArtemisLog";
    static public final String LOG_FILE_DESC = "File to which Artemis output should be sent. Default is ctakes_artemis"
            + ".log";
    @ConfigurationParameter(
            name = LOG_FILE_PARAM,
            description = LOG_FILE_DESC,
            defaultValue = "ctakes_artemis_stopper.log",
            mandatory = false
    )
    private String _logFile;

    static public final String PAUSE_PARAM = "Pause";
    static public final String PAUSE_DESC = "Pause for some seconds after launching.  Default is 0";
    @ConfigurationParameter(
            name = PAUSE_PARAM,
            description = PAUSE_DESC,
            mandatory = false
    )
    private int _pause = 0;


    /**
     * {@inheritDoc}
     */
    @Override
    public void process( final JCas jcas ) throws AnalysisEngineProcessException {
        // Implementation of the process(..) method is mandatory, even if it does nothing.
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void collectionProcessComplete() throws AnalysisEngineProcessException {
        if ( _artemisRoot != null && !_artemisRoot.isEmpty() && !( new File( _artemisRoot ).exists() ) ) {
            LOGGER.warn( "Cannot find Artemis Root Directory " + _artemisRoot );
        }
        try {
            runCommand();
        } catch ( IOException ioE ) {
            throw new AnalysisEngineProcessException( ioE );
        }
    }


    private void runCommand() throws IOException {
        final SystemUtil.CommandRunner runner
                = new SystemUtil.CommandRunner( "bin" + File.separatorChar + "artemis stop" );
        runner.setLogFiles( _logFile, _logFile );
        if ( _artemisRoot != null && !_artemisRoot.isEmpty() ) {
            runner.setDirectory( _artemisRoot );
        }

        LOGGER.info( "Stopping Apache Artemis..." );
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
