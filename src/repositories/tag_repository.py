from src.extensions import db
from src.models.tag import Tag

def get_or_create_tag(name):
    tag = Tag.query.filter_by(name=name).first()
    if not tag:
        tag = Tag(name=name)
        db.session.add(tag)
        db.session.commit()
    return tag
