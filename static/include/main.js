function getCookie(cName) {
	const name = cName + "=";
	const cDecoded = decodeURIComponent(document.cookie);
	const cArr = cDecoded.split('; ');
	let res;
	cArr.forEach(val => {
		if (val.indexOf(name) === 0){
			res = val.substring(name.length);
		}
	})
	return res
}
UserName = document.getElementsByClassName("user-name")[0];
UserImage = document.getElementsByClassName("user-image")[0];
UserName.innerText = getCookie("portal_name").replace(/"/g, '');
UserImage.src = getCookie("portal_picture");
var GlobalYear = 2024;
var UpDown = "up";

ArrowUp = document.getElementById("lineage-up");
ArrowDown = document.getElementById("lineage-down");
ArrowUp.addEventListener("click", function() {
  UpDown = "up";
  ArrowUp.classList.add('highlight-arrow');
  ArrowDown.classList.remove('highlight-arrow');
  if (CurrentItem != 0){
	RemoveAllMarkers();
	DrawRoutes(CurrentItem);  	
  }
});  	
ArrowDown.addEventListener("click", function() {
  UpDown = "down";
  ArrowDown.classList.add('highlight-arrow');
  ArrowUp.classList.remove('highlight-arrow');	
  if (CurrentItem != 0){
	RemoveAllMarkers();
	DrawRoutes(CurrentItem);  	
  }
});   



IconArray = {}
for (Icon of ["Green","Red","Gold","Black","Blue"]){
	var NewIcon = new L.Icon({
	  iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-' + Icon.toLowerCase() + '.png'
	});
	IconArray[Icon] = NewIcon;	
}	
var map = L.map('map',{zoom: 15, minZoom: 2}).setView([0, 0], 2);
//document.getElementsByClassName("leaflet-control-attribution")[0].style.display = "none";
DrawRoutes(0)
DrawRoutesResponseJSON = {}
async function DrawRoutes(ItemDict){ 
    if (ItemDict == 0){
		DrawRoutesResponse = await fetch('/api/v1/GetTaxonomy?key=' + GetKey());
	} else {
		DrawRoutesResponse = await fetch('/api/v1/GetTaxonomy?key=' + GetKey() + '&id=' + ItemDict["ID"] + '&name=' + ItemDict["Name"] + '&group=' + ItemDict["Group"] + '&updown=' + UpDown);	
	}
	DrawRoutesResponseJSON = await DrawRoutesResponse.json();
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    //L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/streets-v11/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZGVraXJrcGF0cmljayIsImEiOiJjaXYzODF3ZWwwMHVrMnBxbnBoOWgweHNoIn0.sRLCN_Ip2WmEzj16Y45kdQ').addTo(map);
    //L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/satellite-streets-v11/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZGVraXJrcGF0cmljayIsImEiOiJjaXYzODF3ZWwwMHVrMnBxbnBoOWgweHNoIn0.sRLCN_Ip2WmEzj16Y45kdQ').addTo(map);
    MinYear = 9999;
    GlobalYear = 2024;
    document.getElementById("CurrentYear").innerText = GlobalYear;
	MarkerPoints = []
    DrawMarkers(DrawRoutesResponseJSON,MinYear);
	document.getElementById("SpinnerDiv").style.display = "none";
	return;
}
//document.getElementById("PlayPause").addEventListener('click', PlayHistory());
function PlayHistory(){
	//console.log(PlayPause);
	if (GlobalYear == 2024){
		Object.entries(DrawRoutesResponseJSON).forEach(([ID, Coords]) => {
			Coords.Events.forEach((Event, Index) => {
				Year = (Event.Date).match(/\b\d{4}\b/);
		  		CurrentYear = Number(Year) ? Year[0] : "";	
		  		if (CurrentYear != ""){
	  				MinYear = Math.min(CurrentYear, MinYear);
	  			}
	  		});
		});
	} else {
		MinYear = GlobalYear;
	}
	PlayPause = document.getElementById("PlayPause");
	MarkerPoints = []
	if (PlayPause.classList.contains('fa-play')){
	  PlayPause.classList.remove('fa-play');
	  PlayPause.classList.add('fa-pause');
		IntervalSetting = 1000;
		TravelThroughTime = setInterval(function() {
		  if (GlobalYear == 2024){
			RemoveAllMarkers();
			DateCounter = 0; 	
		  }
		  MinYear = MinYear + 10;
		  GlobalYear = MinYear;
		  if (MinYear >= 2024){
		  	clearInterval(TravelThroughTime);
	 		PlayPause.classList.remove('fa-pause');
	 		PlayPause.classList.add('fa-play');
		  } else if (MinYear > 1700){
		  	IntervalSetting = 2000;
		  }
		  if (MinYear < 2024){
		  	document.getElementById("CurrentYear").innerText = MinYear
		  } else {
		  	GlobalYear = 2024;
		  	document.getElementById("CurrentYear").innerText = 2024;
		  	clearInterval(TravelThroughTime);
		  }
		  DrawMarkers(DrawRoutesResponseJSON,MinYear);
		  //console.log(MinYear);
		}, IntervalSetting);		
	} else {
	  PlayPause.classList.remove('fa-pause');
	  PlayPause.classList.add('fa-play');
	  clearInterval(TravelThroughTime);
	}
}
 
PolylineGroup = L.featureGroup().addTo(map);   
//MarkersOutput = L.markerClusterGroup();
AllMarkers = [];
AllPolylines = [];
MarkerPoints = [];
DateCounter = 0;


function GetYearFromText(Text){
	Year = (Text).match(/\b\d{4}\b/);
  	CurrentYear = Number(Year) ? Year[0] : "";	
	return CurrentYear;
}

function FastForwardReverse(Direction){
	console.log(Direction);
	if (Direction == "Forward"){
		if (GlobalYear != 2024){
			GlobalYear = Number(GlobalYear) + 10;
		}
	} else {
		GlobalYear = Number(GlobalYear) - 10;		
	}
	DateCounter = 0;
	RemoveAllMarkers();
	DrawMarkers(DrawRoutesResponseJSON,GlobalYear);
	document.getElementById("CurrentYear").innerText = GlobalYear;
}


function DrawMarkers(DrawRoutesResponseJSON,SelectedYear){
	//console.log(DrawRoutesResponseJSON);
	MarkersOutput = L.markerClusterGroup();
	PolylineGroup = L.featureGroup().addTo(map); 
	//console.log(DateCounter+1);
	//console.log(SelectedYear);
	Object.entries(DrawRoutesResponseJSON).forEach(([ID, Coords]) => {
		RouteCoords = []
		Markers = [];
		Coords.Events.forEach((Event, Index) => {
			Markers.push({"latlng": Event.LatLng, "place": Event.Place, "date": Event.Date, "name": Coords.Name, "generation": Coords.Generation, "summary": Coords.Summary})

			RouteCoords.push(Event.LatLng);
		});


		Markers.forEach((marker,index) => {
			CurrentYear = GetYearFromText(marker.date);
  		    if (CurrentYear == ""){
  		    	if (Markers[index - 1] != undefined && Markers[index + 1] != undefined){
  		    		StartDate = GetYearFromText(Markers[index - 1].date);
  		    		EndDate = GetYearFromText(Markers[index + 1].date);
  		    		if (StartDate != "" && EndDate != ""){
  		    			marker.date = "Between " + StartDate + " and " + EndDate;
  		    			CurrentYear = Math.round((Number(StartDate) + Number(EndDate)) / 2);
  		    		}
  		    	}
  		    }
		    if (SelectedYear != 9999 && (CurrentYear > SelectedYear || CurrentYear < (DateCounter + 1))){
		    	return;
		    }

  		    Color = "Black"
  		    if (CurrentYear >= 1900){
  		    	Color = "Green";
  		    } else if (CurrentYear >= 1800){
  		    	Color = "Gold";
  		    } else if (CurrentYear >= 1600){
  		    	Color = "Red";
  		    } else if (CurrentYear >= 1000){
  		    	Color = "Blue";
  		    }
  		    //L.marker([51.5, -0.09], {icon: greenIcon}).addTo(map);i
  		    if (CurrentYear != ""){
  		    	CurrentYear = "<span style='margin-left:20px;'><b>Date: </b>" + marker.date + "</span>";
  		    }
  		    Generation = ""
  		    if (marker.generation != null){
  		   		Generation = '<br><span><b>Generations: </b>' + marker.generation + '</span>';
  		    }
  		    Summary = ""
  		    if (marker.summary != null){
				Summary = '<br>' + (marker.summary).replace(/\*(.*?)\*/g, '<strong>$1</strong>');
  		    }
			var extendedDivIcon = L.divIcon({
				className: 'custom-marker-icon-with-text',
				html: '<img src="' + IconArray[Color].options.iconUrl + '" style="height:41px;width:25px;z-index:9999;position:relative;">' + 
					'<div class="custom-marker-text">' + marker.name + '</div>' +
					'<img class="marker-shadow" src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png" style="width: 41px; height: 41px;">',
				//iconAnchor: [12, 41], // Set the icon anchor
    			//popupAnchor: [1, -34] // Set the popup anchor
			});
 		    var individualMarker = L.marker(marker.latlng, {icon: extendedDivIcon}).bindPopup('<a href="https://www.ancestry.com/family-tree/person/tree/151026520/person/' + ID.replace("0 @I","").replace("@ INDI","") + '/facts" target="_blank">' + marker.name + '</a><br><span><b>Location: </b>' + marker.place + '</span>' + CurrentYear + Generation + "</div><div>" + Summary + "</div>");
 		    //individualMarker.bindLabel('<b>' + marker.name + '</b>').showLabel();
			MarkerPoints.push(marker.latlng)
		    MarkersOutput.addLayer(individualMarker);
   		    if (Markers[index - 1] != undefined){
   		    	Opacity = 0.8;
   		    	if (Color == "Black"){
   		    		Opacity = 0.3;
   		    	}
		    	//L.polyline([marker.latlng, Markers[index + 1]['latlng']], { color: Color, opacity: Opacity }).addTo(map);
		    	L.polyline([marker.latlng, Markers[index - 1]['latlng']], { color: Color, opacity: Opacity }).addTo(PolylineGroup);
		    }
		});
		//route.on('click', function (e) {
		//    route.bindPopup("Route Information").openPopup();
		//});
	});
	//console.log("BOOM");
	map.addLayer(MarkersOutput);
	if (MarkerPoints.length > 0){
		map.fitBounds(L.latLngBounds(MarkerPoints));
	}
	AllMarkers.push(MarkersOutput);
	AllPolylines.push(PolylineGroup)
	DateCounter = SelectedYear;


}

function RemoveAllMarkers(){
    for (Layer of AllMarkers){ 
		map.removeLayer(Layer);
		AllMarkers = [];
	}
	for (Layer of AllPolylines){
		Layer.clearLayers();
		AllPolylines = [];
	}	
}


Preload()
async function Preload(){
	const inputElement = document.getElementById("SearchBox");
	PreloadList = await fetch('/api/v1/GetPeopleList?key=' + GetKey())
	PreloadListArray = await PreloadList.json();
	const instance = typeahead({
		input: inputElement,
		source: {
			local: PreloadListArray,
			identifier: "Name",
			groupIdentifier: "Group"
		},
		display: (item, event) => {
		  if (event) {
		    PickATree(item);
		  }
		  return `${item.Name}`;
		},
		limit: 10,
		highlight: true,
		autoSelect: true,
		hint: true,
		templates: {
			notFound: (resultSet) => `No matches for "${resultSet.query}"`,
			suggestion: function (data) {
				Parents = ""
				if (data.Parents != undefined)
					Parents = '<div style="font-size:10px;">' + data.Parents + '</div>';
		        return '<div>' + data.Name + '</div>' + Parents;
		    }
		}
	});
	//document.getElementsByClassName('tt-list')[0].addEventListener('click', PickATree);
	//document.getElementsByClassName('.typeahead')[0].addEventListener('typeahead:select',PickATree);
}

CurrentItem = 0;
function PickATree(Item) {
	CurrentItem = Item;
	RemoveAllMarkers();
	DrawRoutes(Item);
}

function GetKey(){
  var queryString = window.location.search;
  queryString = queryString.substring(1);
  var queryParams = queryString.split("&");
  for (var i = 0; i < queryParams.length; i++) {
    var pair = queryParams[i].split("=");
    var key = decodeURIComponent(pair[0]);
    var value = decodeURIComponent(pair[1] || '');
    if (key === 'key') {
      return value;
    }
  }
  return null;
}