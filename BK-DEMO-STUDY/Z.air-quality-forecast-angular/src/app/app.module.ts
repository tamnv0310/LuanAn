import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { AngularOpenlayersModule } from 'ngx-openlayers';
 
import { AnalyticComponent } from './analytic/analytic.component';
import { HomeComponent } from './home/home.component';

import {HttpClientModule} from '@angular/common/http';
import { MapviewComponent } from './mapview/mapview.component'

@NgModule({
  declarations: [
    AppComponent,
    AnalyticComponent,
    HomeComponent,
    MapviewComponent  ],
  imports: [
    BrowserModule,
    AppRoutingModule, 
    FormsModule, 
    AngularOpenlayersModule, 
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
