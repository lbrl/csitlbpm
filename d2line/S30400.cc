G4Material* Fe = nist->FindOrBuildMaterial("G4_Fe");
G4Material* Cr = nist->FindOrBuildMaterial("G4_Cr");
G4Material* Ni = nist->FindOrBuildMaterial("G4_Ni");
G4Material* Mn = nist->FindOrBuildMaterial("G4_Mn");
G4Material* Si = nist->FindOrBuildMaterial("G4_Si");
G4Material* N  = nist->FindOrBuildMaterial("G4_N" );
G4Material* C  = nist->FindOrBuildMaterial("G4_C" );
G4Material* P  = nist->FindOrBuildMaterial("G4_P" );
G4Material* S  = nist->FindOrBuildMaterial("G4_S" );

G4double density;
G4int ncomponents;
G4double fractionmass;
/// https://www.makeitfrom.com/material-properties/AISI-304-S30400-Stainless-Steel
G4Material* S30400 = new G4Material("S30400", density= 7.8*g/cm3, ncomponents=9);
S30400->AddElement(Fe, fractionmass=0.7025 );
S30400->AddElement(Cr, fractionmass=0.19   );
S30400->AddElement(Ni, fractionmass=0.0925 );
S30400->AddElement(Mn, fractionmass=0.01   );
S30400->AddElement(Si, fractionmass=0.00375);
S30400->AddElement(N,  fractionmass=0.0005 );
S30400->AddElement(C,  fractionmass=0.0004 );
S30400->AddElement(P,  fractionmass=0.0003 );
S30400->AddElement(S,  fractionmass=0.00015);
