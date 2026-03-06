// Fill out your copyright notice in the Description page of Project Settings.

#define BUILD_SHIPPING 0

#include "VRExpPluginExample.h"

#include "Modules/ModuleManager.h"
#include "NetworkVerOverride.h"

#if !BUILD_SHIPPING
NetworkVerOverride override = NetworkVerOverride();
#endif

IMPLEMENT_PRIMARY_GAME_MODULE( FDefaultGameModuleImpl, VRExpPluginExample, "VRExpPluginExample" );