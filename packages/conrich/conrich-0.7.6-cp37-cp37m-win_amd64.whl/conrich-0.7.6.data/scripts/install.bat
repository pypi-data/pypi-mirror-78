@echo off

if "%PROCESSOR_ARCHITECTURE%"=="x86" (
    regsvr32 /S conrich\Stock\ConcordsCAPIATL.dll
    %WINDIR%/Microsoft.NET/Framework/v4.0.30319/Regasm.exe conrich\Stock\ConcordSTradeAPI.dll /tlb /codebase /register
) else (
    regsvr32 /S conrich\Stock\ConcordsCAPIATLx64.dll
    %WINDIR%/Microsoft.NET/Framework64/v4.0.30319/Regasm.exe conrich\Stock\ConcordSTradeAPI.dll /tlb /codebase /register
)
