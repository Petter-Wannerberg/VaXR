// Fill out your copyright notice in the Description page of Project Settings.


#include "NetworkVerOverride.h"

NetworkVerOverride::NetworkVerOverride()
{
    FNetworkVersion::IsNetworkCompatibleOverride.BindLambda([](uint32 LocalNetworkVersion, uint32 RemoteNetworkVersion)
        {
            return true;
        });
}

NetworkVerOverride::~NetworkVerOverride()
{
}
