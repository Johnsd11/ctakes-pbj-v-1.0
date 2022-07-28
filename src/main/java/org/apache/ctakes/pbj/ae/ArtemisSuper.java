package org.apache.ctakes.pbj.ae;

import org.apache.ctakes.core.pipeline.PipeBitInfo;
import org.apache.log4j.Logger;
import org.apache.uima.analysis_engine.AnalysisEngineProcessException;
import org.apache.uima.fit.component.JCasAnnotator_ImplBase;
import org.apache.uima.jcas.JCas;

/**
 * @author SPF , chip-nlp
 * @since {5/10/2022}
 */
@PipeBitInfo(
        name = "ArtemisSuper",
        description = "Starts an Apache Artemis broker.",
        role = PipeBitInfo.Role.SPECIAL
)
public class ArtemisSuper extends JCasAnnotator_ImplBase {

    static private final Logger LOGGER = Logger.getLogger( "ArtemisSuper" );

    static public final String DIR_PARAM = "ArtemisRoot";
    static public final String DIR_DESC = "Your Artemis root directory.";

    static public final String LOG_FILE_PARAM = "ArtemisLog";
    static public final String LOG_FILE_DESC = "File to which Artemis output should be sent. Default is ctakes_artemis"
            + ".log";

    static public final String PAUSE_PARAM = "Pause";
    static public final String PAUSE_DESC = "Pause for some seconds after launching.  Default is 0";

    /**
     * {@inheritDoc}
     */
    @Override
    public void process( final JCas jcas ) throws AnalysisEngineProcessException {
        // Implementation of the process(..) method is mandatory, even if it does nothing.
    }
}

