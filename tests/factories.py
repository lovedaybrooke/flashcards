import datetime

import factory

from app import models


class VerbStemFactory(factory.Factory):
    class Meta:
        model = models.VerbStem


class VerbPrefixFactory(factory.Factory):
    class Meta:
        model = models.VerbPrefix


class VerbMeaningFactory(factory.Factory):
    class Meta:
        model = models.VerbMeaning


class CombinationFactory(factory.Factory):
    class Meta:
        model = models.Combination


class LearnerFactory(factory.Factory):
    class Meta:
        model = models.Learner


def create_objects_for_testing(db):
    data = [
        LearnerFactory(name="Nigel"),
        VerbPrefixFactory(prefix="dog"),
        VerbPrefixFactory(prefix="cat"),
        VerbPrefixFactory(prefix="fish"),
        VerbStemFactory(stem="make"),
        VerbStemFactory(stem="go"),
        VerbStemFactory(stem="see"),
        VerbStemFactory(stem="eat"),
        VerbMeaningFactory(meaning="create"),
        VerbMeaningFactory(meaning="ignore"),
        VerbMeaningFactory(meaning="sidle"),
        VerbMeaningFactory(meaning="polarise"),
        VerbMeaningFactory(meaning="seafood"),
        VerbMeaningFactory(meaning="meat")
        ]
    for item in data:
        db.session.add(item)
    db.session.commit()

    combinations = [
        CombinationFactory(prefix_id=1, stem_id=1, meaning_id=1),
        CombinationFactory(prefix_id=2, stem_id=1, meaning_id=2),
        CombinationFactory(prefix_id=2, stem_id=2, meaning_id=3),
        CombinationFactory(prefix_id=1, stem_id=3, meaning_id=4),
        CombinationFactory(prefix_id=2, stem_id=3, meaning_id=2),
        CombinationFactory(prefix_id=2, stem_id=4, meaning_id=5),
        CombinationFactory(prefix_id=3, stem_id=4, meaning_id=5),
        CombinationFactory(prefix_id=1, stem_id=4, meaning_id=6),
    ]
    for item in combinations:
        db.session.add(item)
    db.session.commit()
