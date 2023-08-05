

WARNING:
========
Family-Analyzer is outdated and have been replace by pyHam 
available at https://github.com/DessimozLab/pyham . 



Family-Analyzer: summarize gene family evolution from orthoxml 
==============================================================


Motivation 
----------
Family-Analyzer is a tool to further analyze the hierarchical orthologous
groups from an orthoXML file. More informations on the schema of orthoxml and
some examples are available at http://orthoxml.org.

Family-Analyzer report to the user a summary of the evolutionary history acting
on the gene families. The summary reports with respect to one or two levels
taxonomic levels what happens after respectively between the specified
taxonimic levels which genes were maintained, got lost, duplicated, were gained
in that period.


Installation
------------
Family-Analyzer is written in python3, with little external dependencies, i.e.
currently only the lxml library. The setup script should resolve these 
dependencies automatically. 
Consider using pip to install the package directly from a checked out git repo

.. code-block:: sh

   pip install -e </path/to/family-analyzer-repo/>



Running Family-Analyzer
-----------------------
So far running the family analyzer on a specific dataset is relatively easy.
The main entry point for it is the 'main' section in 
familyanalyzer/familyanalyzer.py

If this script is called with -h as argument, it gives a short description 
of the required and optional arguments and what they are used for. Here is
what the usage output reports as of now. Since this is still work in progress,
make sure the current usage did not change.

.. code-block:: sh

   python familyanalyzer/familyanalyzer.py -h
   
   usage: familyanalyzer.py [-h] [--xreftag XREFTAG] [--show_levels] [-r]
                            [--taxonomy TAXONOMY] [--propagate_top]
                            [--show_taxonomy]
                            [--store_augmented_xml STORE_AUGMENTED_XML]
                            [--compare_second_level COMPARE_SECOND_LEVEL]
                            orthoxml level species [species ...]
   
   Analyze Hierarchical OrthoXML families.
   
   positional arguments:
     orthoxml              path to orthoxml file to be analyzed
     level                 taxonomic level at which analysis should be done
     species               (list of) species to be analyzed. Note that only genes
                           of the selected species are reported. In order for the
                           output to make sense, the selected species all must be
                           part of the linages specified in 'level' (and
                           --compare_second_level).
   
   optional arguments:
     -h, --help            show this help message and exit
     --xreftag XREFTAG     xref tag of genes to report. OrthoXML allows to store
                           multiple ids and xref annotations per gene as
                           attributes in the species section. If not set, the
                           internal (purely numerical) ids are reported.
     --show_levels         print the levels and species found in the orthoXML
                           file and quit
     -r, --use-recursion   DEPRECATED: Use recursion to sample families that are
                           a subset of the query
     --taxonomy TAXONOMY   Taxonomy used to reconstruct intermediate levels. Has
                           to be either 'implicit' (default) or a path to a file
                           in Newick format. The taxonomy might be
                           multifurcating. If set to 'implicit', the taxonomy is
                           extracted from the input OrthoXML file. The orthoXML
                           level do not have to cover all the levels for all
                           families. In order to infer gene losses Family-
                           Analyzer needs to infer these skipped levels and
                           reconcile each family with the complete taxonomy.
     --propagate_top       propagate taxonomy levels up to the toplevel. As an
                           illustration, consider a gene family in an eukaryotic
                           analysis that has only mammalian genes. Its topmost
                           taxonomic level will therefor be 'Mammalia' and an
                           ancestral gene was gained at that level. However, if
                           '--propagete-top' is set, the family is assumed to
                           have already be present in the topmost taxonomic
                           level, i.e. Eukaryota in this example, and non-
                           mammalian species have all lost this gene.
     --show_taxonomy       write the taxonomy used to standard out.
     --store_augmented_xml STORE_AUGMENTED_XML
                           filename to which the input orthoxml file with
                           augmented annotations is written. The augmented
                           annotations include for example the additional
                           taxonomic levels of orthologGroup and unique HOG IDs.
     --compare_second_level COMPARE_SECOND_LEVEL
                           Compare secondary level with primary one, i.e. report
                           what happend between the secondary and primary level
                           to the individual histories. Note that the Second
                           level needs to be younger than the primary.


Code organisation
-----------------

OrthoXMLParser: class which holds the orthoxml file and gives access to its 
                data and keeps internal mappings to speed up lookups.


Taxonomy: class wich provides a basic navigation through the species taxonomy.
          Objects will be constructed using the TaxonomyFactory and can be 
          either based on the orthoxml or a newick tree. 
