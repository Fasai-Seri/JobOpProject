const ShowMap = () => {
    const data = document.getElementById("create_job_post_script").dataset;
  
    function Map() {
      const mapContainer = React.useRef();
      const map = React.useRef();
      const marker = React.useRef();
      const compAdd = React.useRef({});
      const [center] = React.useState([100.530285, 13.734024]);
      const [zoom] = React.useState(14);
      const [API_KEY] = React.useState("GofhIpWUfkKFYIIo84aL");
      maptilersdk.config.apiKey = "GofhIpWUfkKFYIIo84aL";
      React.useEffect(() => {
        if (map.current) return;
        if (!mapContainer.current) return;
        map.current = new maptilersdk.Map({
          container: mapContainer.current,
          style: `https://api.maptiler.com/maps/streets-v2/style.json?key=${API_KEY}`,
          center: center,
          zoom: zoom,
        });
  
        marker.current = new maptilersdk.Marker({ color: "#FF0000" })
          .setLngLat(center)
          .addTo(map.current);
  
        const gc = new maptilersdkMaptilerGeocoder.GeocodingControl();
  
        map.current.addControl(gc, "top-left");
  
        map.current.on("click", async function (e) {
          if (marker.current) {
            marker.current.remove();
          }
  
          marker.current = new maplibregl.Marker({ color: "#FF0000" })
            .setLngLat([e.lngLat.lng, e.lngLat.lat])
            .addTo(map.current);
          const results = await maptilersdk.geocoding.reverse([
            e.lngLat.lng,
            e.lngLat.lat,
          ]);
          document.getElementById("info").innerHTML =
            JSON.stringify(results.features[0].place_name_en) +
            "<br />" +
            JSON.stringify(e.lngLat.wrap());
          document.getElementById("job_address").innerHTML = String(
            results.features[0].place_name_en
          );
          document.getElementById("job_location_long").value = e.lngLat.lng;
          document.getElementById("job_location_lat").value = e.lngLat.lat;
          compAdd.current = {
            job_location_long: e.lngLat.lng,
            job_location_lat: e.lngLat.lat,
            job_address: results.features[0].place_name_en,
          };
          console.log(compAdd);
        });
      }, [API_KEY, center, zoom]);
  
      return (
        <div>
          <div class="form-group">
            <label for="comp_name">Company Address</label>
            <textarea
              type="text"
              class="form-control"
              id="job_address"
              name="job_address"
              placeholder="Company Address"
              required
            ></textarea>
          </div>
          <input type="hidden" id="job_location_long" name="job_location_long" />
          <input type="hidden" id="job_location_lat" name="job_location_lat" />
          <pre
            id="info"
            class="position-relative d-block w-75 p-2 mt-2 rounded"
          ></pre>
          <div ref={mapContainer} class="position-absolute w-100 h-50" />
        </div>
      );
    }
  
    return (
      <div>
          <Map />
      </div>
    );
  };
  
  ReactDOM.render(<ShowMap />, document.querySelector("#job_location"));
  