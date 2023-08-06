# texta-parsers

A Python package for general file parsing. Most of the file types are parsed with **[tika](http://tika.apache.org/)**. 
However, since tika does not support everything and for some file types more sophisticated parsing is more beneficial, some other tools are required as well:

* **pst-utils** - converts .pst to .mbox
* **digidoc-tool** - extracts files from Estonian digital signature containers

The package contains two parsers. These are **DocParser** and **EmailParser**. 


## Requirements

Requires *pst-utils*, *digidoc-tool* and *lxml* for parsing mailboxes, digidocs and XML (*lxml* is not needed if Conda environment is used):

`sudo apt-get install pst-utils python3-lxml -y`

`sudo sh install-digidoc.sh`

Requires our custom version of Apache TIKA with relevant Tesseract language packs installed:

`sudo docker run -p 9998:9998 docker.texta.ee/texta/texta-parsers-python/tikaserver:latest`

For using MLP:

`pip install texta-mlp`


## Testing

`python -m  pytest -rx -v tests`


## Description

#### DocParser

A parser for general file parsing. Input can either be in bytes or a path to the file as a string. See [user guide](https://git.texta.ee/texta/email-parser/-/wikis/DocParser/User-Guide/Getting-started) more information. DocParser also includes EmailParser.

#### EmailParser

A parser that parses email messages and mailboxes. Supported file formats are Outlook Data File (**.pst**), mbox (**.mbox**) and EML (**.eml**). Can be used separately from DocParser.
User guide can be found [here](https://git.texta.ee/texta/email-parser/-/wikis/EmailParser/User-Guide/Getting-started) and documentation [here](https://git.texta.ee/texta/email-parser/-/wikis/EmailParser/Documentation/1.2.1).


#### Entity Linker Pipeline

EntityLinkers wrapper can only be used if the previous generator passed through
it belongs to the MLP processor (it needs mlp-processed documents to function).

In the following example, the mailbox "Корзина.mbox" will be parsed by the EmailParser,
processed by the Texta MLP worker to enhance the text with additional information about its entities.
Those entities are then loaded into the memory to be used as the Entity Linkers input.

Finally the entity linked results will be passed over to the Elasticsearch worker, to save them into an index
of the users choice (note that mapping problems might happen when pushing into an already existing index)

*For this example, an install of the texta-mlp package and a running instance of our Tika build is necessary.*

```python
from texta_mlp.mlp import MLP

from texta_parsers.email_parser import EmailParser
from texta_parsers.tools.entity_linker_wrapper import EntityLinkerWrapper
from texta_parsers.tools.elastic import ESImporter
from texta_parsers.tools.mlp_processor import MLPProcessor

index_name = "personage_info"

mlp = MLP(language_codes=["et", "en", "ru"])
concat_wrapper = EntityLinkerWrapper()
mlp_wrapper = MLPProcessor(mlp)
elastic_importer = ESImporter("http://localhost:9200", index_prefix="rus")
email_parser = EmailParser()

generator = email_parser.parse("tests/data/Корзина.mbox")
generator = mlp_wrapper.apply_mlp(generator)

# Generator takes input in the form of a tuple containing the mlp output dictionary and a list (for attachments).
generator = concat_wrapper.concat_from_generator(generator)
pipeline_end = elastic_importer.push_linked_entities_into_elastic(generator, index_name)
```

All the entity-linked information should not be in an index named "personage_info"

