const CreateCompany = () => {
  const [previewLogo, setPreviewLogo] = React.useState("");
  const data = document.getElementById("create_company_script").dataset;
  const csrftoken = data.csrfToken;

  function handlePreviewLogo() {
    const logo = document.querySelector("#comp_logo").files[0];
    setPreviewLogo(URL.createObjectURL(logo));
  }

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
        document.getElementById("comp_address").innerHTML = String(
          results.features[0].place_name_en
        );
        document.getElementById("comp_long").value = e.lngLat.lng;
        document.getElementById("comp_lat").value = e.lngLat.lat;
        compAdd.current = {
          comp_long: e.lngLat.lng,
          comp_lat: e.lngLat.lat,
          comp_address: results.features[0].place_name_en,
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
            id="comp_address"
            name="comp_address"
            placeholder="Company Address"
            required
          ></textarea>
        </div>
        <input type="hidden" id="comp_long" name="comp_long" />
        <input type="hidden" id="comp_lat" name="comp_lat" />
        <pre
          id="info"
          class="position-relative d-block w-75 p-2 mt-2 rounded"
        ></pre>
        <div ref={mapContainer} class="position-absolute w-100 h-50" />
      </div>
    );
  }

  return (
    <div class="container mt-3">
      <div class="row justify-content-center">
        <div class="col-md-12">
          <div class="mb-3 bg-light p-4 rounded shadow-sm">
            <h4>Create Company</h4>
            <hr />
            {previewLogo ? (
              <img
                class="rounded-circle"
                src={previewLogo}
                width="200"
                height="200"
              />
            ) : (
              <img
                class="rounded-circle"
                src="media\company\Images\default.jpg"
                width="200"
                height="200"
              />
            )}
            <form id="comp_form" method="post" enctype="multipart/form-data">
              <input
                type="hidden"
                name="csrfmiddlewaretoken"
                value={csrftoken}
              />
              <div>
                <input
                  type="file"
                  class="form-control-file"
                  id="comp_logo"
                  name="comp_logo"
                  onChange={handlePreviewLogo}
                />
              </div>
              <div class="form-group">
                Company Name:{" "}
                <input class="form-control" name="comp_name" required />
              </div>
              <div class="form-group">
                Company Thai Name:{" "}
                <input class="form-control" name="comp_name_th" />
              </div>
              <div class="form-group">
                Company Description:{" "}
                <textarea class="form-control" name="comp_desc"></textarea>
              </div>

              <div class="form-group">
                Company Contact Info:{" "}
                <textarea
                  class="form-control"
                  name="comp_contact_info"
                  required
                ></textarea>
              </div>
              <input type="submit" class="btn btn-primary" value="Create" />
              <Map />
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

ReactDOM.render(<CreateCompany />, document.querySelector("#create_company"));
