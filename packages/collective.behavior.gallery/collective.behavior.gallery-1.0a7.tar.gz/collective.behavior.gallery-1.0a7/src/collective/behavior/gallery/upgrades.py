# -*- coding: utf-8 -*-
from plone.app.upgrade.utils import loadMigrationProfile


def reload_gs_profile(context):
    loadMigrationProfile(
        context,
        'profile-collective.behavior.gallery:default',
    )


def reload_registry_profile(context):
    context.runImportStepFromProfile(
        'profile-collective.behavior.gallery:default',
        'plone.app.registry'
    )
