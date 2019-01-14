#include "TH2D.h"
#include "TH2S.h"
#include "TFile.h"

int hp( string inname, string outname ){
    int nx = 1600, ny = 1200;
    ////////////////////////////////////
    auto fin = new TFile( inname.c_str() );
    auto hin = (TH2S *) fin->Get( "t1" );
    // auto fout = new TFile( outname.c_str(), "recreate" );
    TH2D * hout = 0;
    hout = (TH2D *) hin->Clone();
    // TH2D * hout = new TH2D( "t1", "hp", nx, 0, nx, ny, 0, ny );
    // TH2S * hout = new TH2S( "t1", "hp", nx, 0, nx, ny, 0, ny );
    ////////////////////////////////////
    double bc, s, neis[8];
    double kx[] = {-1, 0, 1,  -1, 1,  -1,  0,  1};
    double ky[] = { 1, 1, 1,   0, 0,  -1, -1, -1};
    double nei_ave, nei_rms;
    ////////////////////////////////////
    nei_ave = hin->GetBinContent( 691, 309 );
    nei_ave += hin->GetBinContent( 691, 310 );
    nei_ave += hin->GetBinContent( 698, 309 );
    nei_ave += hin->GetBinContent( 698, 310 );
    nei_ave /= 4.;
    if( hin->GetBinContent( 694, 309 ) > nei_ave*2 ){
        hout->SetBinContent( 693, 309, nei_ave );
        hout->SetBinContent( 694, 309, nei_ave );
        hout->SetBinContent( 695, 309, nei_ave );
    }
    if( hin->GetBinContent( 694, 310 ) > nei_ave*2 ){
        hout->SetBinContent( 693, 310, nei_ave );
        hout->SetBinContent( 694, 310, nei_ave );
        hout->SetBinContent( 695, 310, nei_ave );
    }
    ////////////////////////////////////
    for( int i=2; i<nx-1; i++ ){
        for( int j=2; j<ny-1; j++ ){
            bc = hin->GetBinContent( i, j );
            nei_ave = 0.;
            for( int k=0; k<8; k++ ){
                neis[k] = hin->GetBinContent( i+kx[k], j+ky[k] );
                nei_ave += neis[k];
            }
            nei_ave /= 8.;
            nei_rms = 0.;
            for( int k=0; k<8; k++ ){
                nei_rms += pow( neis[k]-nei_ave, 2 );
            }
            nei_rms = sqrt( nei_rms/8. );
            if( fabs(bc-nei_ave) > 10*nei_rms ){
                hout->SetBinContent( i, j, nei_ave );
            }
        }
    }
    ////////////////////////////////////
    hout->SaveAs( outname.c_str() );
    fin->Close();
    // hout->Write();
    // fout->Close();
    return 0;
}
