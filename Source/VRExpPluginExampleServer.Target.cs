// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;
using System.Collections.Generic;

[SupportedPlatforms(UnrealPlatformClass.Server)]
public class VRExpPluginExampleServerTarget : TargetRules
{
	public VRExpPluginExampleServerTarget(TargetInfo Target) : base(Target)
	{
        DefaultBuildSettings = BuildSettingsVersion.V2;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;

		Type = TargetType.Server;

		ExtraModuleNames.AddRange(new string[] { "VRExpPluginExample" });

		// LyraGameTarget.ApplySharedLyraTargetSettings(this);

		//bUseChecksInShipping = true;

        ProjectDefinitions.Add("UE_PROJECT_STEAMSHIPPINGID=480");
	}
}
