// Copyright 2017-present, Institute for Artificial Intelligence - University of Bremen
// Author: Andrei Haidu (http://haidu.eu)

using UnrealBuildTool;
using System.Collections.Generic;

public class RobCoGEditorTarget : TargetRules
{
	public RobCoGEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;        
        //DefaultBuildSettings = BuildSettingsVersion.V2;

		ExtraModuleNames.AddRange( new string[] { "RobCoG" } );
	}
}
