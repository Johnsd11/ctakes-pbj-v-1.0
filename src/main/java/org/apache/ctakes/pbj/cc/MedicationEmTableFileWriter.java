package org.apache.ctakes.pbj.cc;

import org.apache.ctakes.core.cc.AbstractTableFileWriter;
import org.apache.ctakes.core.pipeline.PipeBitInfo;
import org.apache.ctakes.core.util.annotation.IdentifiedAnnotationUtil;
import org.apache.ctakes.typesystem.type.refsem.Attribute;
import org.apache.ctakes.typesystem.type.textsem.MedicationEventMention;
import org.apache.uima.cas.FeatureStructure;
import org.apache.uima.fit.util.JCasUtil;
import org.apache.uima.jcas.JCas;
import org.apache.uima.jcas.cas.FSArray;
import org.apache.uima.jcas.tcas.Annotation;

import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.stream.Collectors;

import static org.apache.ctakes.core.pipeline.PipeBitInfo.TypeProduct.*;

@PipeBitInfo(
      name = "Medication Event Mention Table Writer",
      description = "Writes a table of Medication information to file, sorted by character index.",
      role = PipeBitInfo.Role.WRITER,
      dependencies = { DOCUMENT_ID, IDENTIFIED_ANNOTATION },
      usables = { DOCUMENT_ID_PREFIX }
)
public class MedicationEmTableFileWriter extends AbstractTableFileWriter {
// test line for checkin, post infra https://issues.apache.org/jira/browse/INFRA-21596

   /**
    * {@inheritDoc}
    */
   @Override
   protected List<String> createHeaderRow( final JCas jCas ) {
      return Arrays.asList(
            " Preferred Text ",
            " Document Text ",
            " Strength ",
            " Dose ",
            " Form ",
            " Route ",
            " Frequency ",
            " Duration " );
   }

   /**
    * {@inheritDoc}
    */
   @Override
   protected List<List<String>> createDataRows( final JCas jCas ) {
      return JCasUtil.select( jCas, MedicationEventMention.class )
                     .stream()
                     .sorted( Comparator.comparingInt( Annotation::getBegin ) )
                     .map( ModifierRow::new )
                     .map( ModifierRow::getColumns )
                     .collect( Collectors.toList() );
   }


   /**
    * Simple container for annotation information.
    */
   static private class ModifierRow {

      private final String _prefText;
      private final String _docText;
      private final String _strength;
      private final String _dose;
      private final String _form;
      private final String _route;
      private final String _frequency;
      private final String _duration;

      static private String getText( final Attribute attribute ) {
         if ( attribute == null ) {
            return "";
         }
         final FSArray mentions = attribute.getMentions();
         if ( mentions == null || mentions.size() == 0 ) {
            return "";
         }
         final FeatureStructure mention = mentions.get( 0 );
         if ( mention instanceof Annotation ) {
            return ( (Annotation) mention ).getCoveredText();
         }
         return "";
      }

      private ModifierRow( final MedicationEventMention med ) {
         _prefText = IdentifiedAnnotationUtil.getPreferredTexts( med )
                                             .stream()
                                             .sorted()
                                             .collect( Collectors.joining( ";" ) );
         _docText = med.getCoveredText();
         _strength = getText( med.getMedicationStrength() );
         _dose = getText( med.getMedicationDosage() );
         _form = getText( med.getMedicationForm() );
         _route = getText( med.getMedicationRoute() );
         _frequency = getText( med.getMedicationFrequency() );
         _duration = getText( med.getMedicationDuration() );
      }

      public List<String> getColumns() {
         return Arrays.asList(
               _prefText,
               _docText,
               _strength,
               _dose,
               _form,
               _route,
               _frequency.replace( " null", "" ),
               _duration );
      }

   }


}

