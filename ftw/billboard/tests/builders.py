from ftw.builder.archetypes import ArchetypesBuilder
from ftw.builder import builder_registry


class AdCategoryBuilder(ArchetypesBuilder):
    portal_type = 'BillboardCategory'


builder_registry.register('billboard category', AdCategoryBuilder)


class AdBuilder(ArchetypesBuilder):
    portal_type = 'BillboardAd'


builder_registry.register('billboard ad', AdBuilder)
