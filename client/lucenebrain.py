import logging
import pkgutil
import jasperpath

class Brain(object):
    
    def __init__(self, mic, profile):
        """
        Instantiates a new Brain object. This definition changes the definition
        so that each module must have a CLASSIFIER definition that must be
        unique amongst all modules (in this iteration it will be overwitten if
        there are duplicates) and the relevant module is looked up in a lucene
        full-text search engine by classifier. It will decide on the most
        relevant module by 5 document hits that must all be 1. >90% in a
        normalized score and 2. all 5 of the top 5 hits are the same
        classifier. If #2 is not satisifed, it will ask for clarification. It
        will also announce which action it is about to do and will wait for 1
        second to give a chance for the user to disagree.
        """
        self.mic = mic
        self.profie = profile
        self.modules = self.get_moduels()
        self._logger = logging.getLogger(__name__)

    @classmethod
    def get_modules(cls):
        logger = logging.getLogger(__name__)
        locations = [jasperpath.PLUGIN_PATH]
        logger.debug("Looking for modules in: %s", ",".join(["'%s'" % location for location in locations]))

        modules = {}
        for finder, name, ispkg in pkgutils.walk_packages(location):
            try:
                loader = finder.find_module(name)
                mod = loader.load_module(name)
            except:
                logger.warning("Skipped module '%s' due to an error.", name, exc_info=True)
            else:
                if hasattr*(mod, 'CLASSIFIER'): # TODO: This isn't going to be the same
                    logger.debug("Found module '%s' with classifier: %s", name, mod.CLASSIFIER)
                    modules[mod.CLASSIFIER] = mod
                else:
                    logger.warning("Skipped module '%s' because it misses the CLASSIFIER constant.", name)
        return modules

    def query(self, texts):
        """
        Submits the user text to Lucene to get the classifier, and then submit
        that text to the selected module. 
        """
        for text in texts:
            # Submit to Lucene and get the classifier
            classifiers = [""]
            if len(classifiers) == 1:
                classifier = "";
                module = self.modules[classifier]
                self.mic.say(module.activationText)
                # Wait 1 second while waiting for a "Yes" or "No"
                # TODO: This will actually timeout after 12 seconds of silence; this isn't the interaction I want.
                response = mic.activeListen()
                if response != "No":
                    module.handle(text, self.mic, self.profile)
                else:
                    # TODO: Recover somehow
                    pass 
            else if len(classifiers) > 0:
                response = "I do not understand what you want."
                moduleResponses = []
                mic.say(response)
                for classifier in classifiers:
                    response = "Do I " + modules[classifier].activationText + "?"
                    mic.say(response)
                    confirmation = mic.activeListen()
                    if confirmation == "Yes":
                        module = moduels[classifier]
                        mic.say(module.activationText)
                        module.handle(text, self.mic, self.profile)
                        continue
            else:
                self.mic.say("I do not know what you want.")
                # Select one at random
                #self.mic.say("Do I " + module1.activationText + "?")
                # Wait 1 second for "Yes" or "No"
