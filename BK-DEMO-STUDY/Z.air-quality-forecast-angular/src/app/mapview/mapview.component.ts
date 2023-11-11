import { Component, OnInit } from '@angular/core';
// import { map } from 'rxjs/operators';

import { Map, View } from 'ol';
import { Tile as TileLayer, Vector as VectorLayer } from 'ol/layer';
import { XYZ, Vector as VectorSource } from 'ol/source';
import { Style, Fill, Stroke, Circle } from 'ol/style';
import { GeoJSON } from 'ol/format';
import { click, singleClick } from 'ol/events/condition';
import Select from 'ol/interaction/Select';

@Component({
  selector: 'app-mapview',
  templateUrl: './mapview.component.html',
  styleUrls: ['./mapview.component.scss']
})
export class MapviewComponent implements OnInit {
  // map: Map;
  vectorSource: VectorSource = new VectorSource();
  
  constructor( public map: Map) { 
  }

  ngOnInit(): void {
    this.map = new Map({
      target: 'map',
      layers: [
        new TileLayer({
          source: new XYZ({ url: 'https://{a-c}.tile.osm.org/{z}/{x}/{y}.png' })
        }),
        // new VectorLayer({
        //   url: 'https://openlayers.org/en/latest/examples/data/geojson/countries.geojson',
        //   format: new GeoJSON()
        // })
      ],
      view: new View({
        center: [288626, 5885039],
        zoom: 5
      })
    });
  }

}



new Map({
  target: 'map',
  layers: [
    new TileLayer({
      source: new XYZ({
        url: 'https://{a-c}.tile.openstreetmap.org/{z}/{x}/{y}.png'
      })
    })
  ],
  view: new View({
    center: [0, 0],
    zoom: 2
  })
});