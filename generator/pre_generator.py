from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm.attributes import InstrumentedAttribute


def is_geo_class(a_class:DeclarativeMeta):
    model_attrs = [getattr(a_class, element) for element in dir(a_class) if isinstance(getattr(a_class, element), InstrumentedAttribute)]
    for attr in model_attrs:
        try:
            if(hasattr(attr.property.columns[0].type, "geometry_type")):
                return True
        except AttributeError:
            pass
            # for ele in dir(attr.property):
            #     print(ele)
        # print()
    return False