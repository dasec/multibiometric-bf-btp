# Multi-Biometric Template Protection based on Bloom filters

Implementation of the feature level fusion of Bloom filter based protected templates proposed in [[IF18]](http://www.sciencedirect.com/science/article/pii/S1566253516301233) .

## License
This work is licensed under license agreement provided by Hochschule Darmstadt ([h_da-License](/hda-license.pdf)).

## Instructions

### Dependencies
* seaborn
* numpy
* pylab
* matplotlib
* argparse

### Usage

1. Run BF_template_fusion.py to fuse the Bloom filter based templates of two characteristics or instances. 

	```python
	usage: BF_template_fusion.py [-h]
                                 [--DB_BFtemplates_fused [DB_BFTEMPLATES_FUSED]]
                                 DB_BFtemplatesA DB_BFtemplatesB fusionList
    
    Extract unprotected LGBPHS and protected Bloom filter templates from the FERET
    DB.
    
    positional arguments:
      DB_BFtemplatesA       directory where the protected BF templates for
                            characteristic A are stored
      DB_BFtemplatesB       directory where the protected BF templates for
                            characteristic B are stored
      fusionList            file where the pairs of templates to be fused are
                            specified

    optional arguments:
      -h, --help            show this help message and exit
      --DB_BFtemplates_fused [DB_BFTEMPLATES_FUSED]
                            directory where the protected fused BF templates will
                            be stored
	```

	1. Input: at least 2 directories where the protected templates to be fused are stored, and a file with the list of templates to be fused. Each line of the file contains the corresponding file names separated by a blank space. It should be noted that the first characteristic should be the one comprising the biggest templates (iris in the example).
	2. Output: fused templates, stored in the directory indicated by DB_BFtemplates_fused.
	3. Two templates have been provided to show how the script works. The call should be: ```BF_template_fusion.py irisDB/ faceDB/ fusionList.txt```

2. Run BF_template_fusion.py to fuse the Bloom filter based templates of two characteristics or instances. 

	```python
    usage: computeScores.py [-h] [--scoresDir [SCORESDIR]]
                            [--matedScoresFile [MATEDSCORESFILE]]
                            [--nonMatedScoresFile [NONMATEDSCORESFILE]]
                            DB_BFtemplates matedComparisonsFile
                            nonMatedComparisonsFile
    
    Compute protected Bloom filter scores from a given DB and protocol.
    
    positional arguments:
      DB_BFtemplates        directory where the protected BF templates are stored
      matedComparisonsFile  file comprising the mated comparisons to be carried
                            out
      nonMatedComparisonsFile
                            file comprising the non-mated comparisons to be
                            carried out
    
    optional arguments:
      -h, --help            show this help message and exit
      --scoresDir [SCORESDIR]
                            directory where unprotected and protected scores will
                            be stored
      --matedScoresFile [MATEDSCORESFILE]
                            file comprising the mated scores computed
      --nonMatedScoresFile [NONMATEDSCORESFILE]
                            file comprising the non-mated scores computed
    ```
    1. Input: folders with the unprotected and protected templates (arguments can be modified at the top of the script to use other folders), as well as the folder where the scores will be stored
	2. Output: mated and non-mated scores, stored in text files with one score per row

## References

More details in:

- [[IF18]](http://www.sciencedirect.com/science/article/pii/S1566253516301233) M. Gomez-Barrero, C. Rathgeb, G. Li, R. Raghavendra, J. Galbally and C. Busch, "Multi-Biometric Template Protection 
Based on Bloom Filters", in Information Fusion, vol. 42, pp. 37-50, 2018.

Please remember to reference article [IF18] on any work made public, whatever the form,
based directly or indirectly on these scripts.