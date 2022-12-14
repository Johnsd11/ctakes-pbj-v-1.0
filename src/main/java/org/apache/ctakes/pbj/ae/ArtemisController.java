package org.apache.ctakes.pbj.ae;

import org.apache.ctakes.core.pipeline.PipeBitInfo;
import org.apache.log4j.Logger;
import org.apache.uima.UimaContext;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.fit.component.JCasAnnotator_ImplBase;
import org.apache.uima.fit.descriptor.ConfigurationParameter;
import org.apache.uima.jcas.JCas;
import org.apache.uima.resource.ResourceInitializationException;

import java.io.File;
import java.io.IOException;

/**
 * @author SPF , chip-nlp
 * @since {5/10/2022}
 */
@PipeBitInfo(
        name = "ArtemisController",
        description = "Controls the broker.",
        role = PipeBitInfo.Role.SPECIAL
)

abstract public class ArtemisController extends JCasAnnotator_ImplBase {

    static private final Logger LOGGER = Logger.getLogger( "ArtemisSuper" );

    static public final String DIR_PARAM = "ArtemisRoot";
    static public final String DIR_DESC = "Your Artemis root directory.";

    @ConfigurationParameter(
            name = DIR_PARAM,
            description = DIR_DESC,
            mandatory = false
    )
    protected String _artemisRoot;

    static public final String LOG_FILE_PARAM = "ArtemisLog";
    static public final String LOG_FILE_DESC = "File to which Artemis output should be sent. Default is ctakes_artemis"
            + ".log";
    static public final String LOG_FILE_DEFAULT = "ctakes_artemis_controller.log";
    @ConfigurationParameter(
            name = LOG_FILE_PARAM,
            description = LOG_FILE_DESC,
            defaultValue = LOG_FILE_DEFAULT,
            mandatory = false
    )
    protected String _logFile;

    static public final String PAUSE_PARAM = "Pause";
    static public final String PAUSE_DESC = "Pause for some seconds after launching.  Default is 0";


    @ConfigurationParameter(
            name = PAUSE_PARAM,
            description = PAUSE_DESC,
            mandatory = false
    )
    protected int _pause = 0;




    /**
     * {@inheritDoc}
     */
    @Override
    public void initialize( final UimaContext context ) throws ResourceInitializationException {
        super.initialize( context );
    }





}

