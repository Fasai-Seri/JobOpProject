const CompanyProfile = () => {
  const [company, setCompany] = React.useState({});
  const compAdd = React.useRef({});
  const [posts, setPosts] = React.useState([]);
  const [isDisabled, setIsDiabled] = React.useState("true");
  const [previewLogo, setPreviewLogo] = React.useState("");
  const data = document.getElementById("company_script").dataset;
  const comp_id = parseInt(data.compId, 10);
  const csrftoken = data.csrfToken;
  const post_href = data.postHref.slice(0, -1);

  React.useEffect(() => {
    fetch_company();
    fetch_company_posts();
  }, []);

  function fetch_company() {
    fetch(`get_company/${comp_id}`)
      .then((response) => response.json())
      .then((comp) => {
        setCompany(comp);
      });
  }

  function fetch_company_posts() {
    fetch(`get_company_job_posts/${comp_id}`)
      .then((response) => response.json())
      .then((posts) => {
        setPosts(posts);
      });
  }

  function handleLogoPreview() {
    const logo = document.querySelector("#comp_logo").files[0];
    setPreviewLogo(URL.createObjectURL(logo));
  }

  function handleCompanyChange(e) {
    const { name, value } = e.target;
    setCompany((prevComp) => ({
      ...prevComp,
      [name]: value,
    }));
  }

  function handleCompanySubmit() {
    if (compAdd.current) {
      fetch(`update_company/${comp_id}`, {
        method: "POST",
        body: JSON.stringify({
          comp_name: company.comp_name,
          comp_name_th: company.comp_name_th,
          comp_desc: company.comp_desc,
          comp_address: compAdd.current.comp_address,
          comp_long: compAdd.current.comp_long,
          comp_lat: compAdd.current.comp_lat,
          comp_contact_info: company.comp_contact_info,
        }),
      });
    } else {
      fetch(`update_company/${comp_id}`, {
        method: "POST",
        body: JSON.stringify({
          comp_name: company.comp_name,
          comp_name_th: company.comp_name_th,
          comp_desc: company.comp_desc,
          comp_address: company.comp_address,
          comp_long: company.comp_long,
          comp_lat: company.comp_lat,
          comp_contact_info: company.comp_contact_info,
        }),
      });
    }
  }

  function handleLogoUpload() {
    const logo = document.querySelector("#comp_logo").files[0];
    if (logo) {
      const formData = new FormData();
      formData.append("comp_logo", logo);
      fetch(`update_comp_logo/${comp_id}`, {
        method: "POST",
        body: formData,
      });
    }
  }

  function handleEditCompClick() {
    setIsDiabled("false");
  }
  function handleCancleCompClick() {
    fetch_company();
    setIsDiabled("true");
    setPreviewLogo("");
  }

  function PostSection(props) {
    return (
      <div>
        <img
          src={props.post.company_logo}
          class="rounded-circle"
          width="100px"
          height="100px"
        />
        <a href={post_href + "/" + props.post.job_id}>{props.post.job_title}</a>
        <p>{props.post.job_type}</p>
        <p>{props.post.company}</p>
        <p>{props.post.job_location}</p>
        <p>Posted date: {props.post.job_post_date}</p>
        <p>
          Close date:{" "}
          {props.post.job_close_date ? props.post.job_close_date : "-"}
        </p>
      </div>
    );
  }
  console.log(company);
  console.log(compAdd);

  function Map(props) {
    const mapContainer = React.useRef();
    const map = React.useRef();
    const marker = React.useRef();
    const [center] = React.useState([props.long, props.lat]);
    const [zoom] = React.useState(14);
    const [API_KEY] = React.useState("GofhIpWUfkKFYIIo84aL");
    maptilersdk.config.apiKey = "GofhIpWUfkKFYIIo84aL";

    if (!props.lat | !props.long) return <div></div>;
    React.useEffect(() => {
      if (map.current) return;
      if (!mapContainer.current) return;
      map.current = new maplibregl.Map({
        container: mapContainer.current,
        style: `https://api.maptiler.com/maps/streets-v2/style.json?key=${API_KEY}`,
        center: center,
        zoom: zoom,
      });

      marker.current = new maplibregl.Marker({ color: "#FF0000" })
        .setLngLat(center)
        .addTo(map.current);

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
        compAdd.current = {
          comp_long: e.lngLat.lng,
          comp_lat: e.lngLat.lat,
          comp_address: results.features[0].place_name_en,
        };
        console.log(company);
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
            disabled={isDisabled == "true" ? true : false}
            placeholder="Company Address"
            value={company.comp_address}
            required
          ></textarea>
        </div>
        <pre
          id="info"
          class="position-relative d-block w-75 p-2 mt-2 rounded"
        ></pre>
        <div ref={mapContainer} class="position-absolute w-100 h-50" />
      </div>
    );
  }

  function textAreaAdjust(e) {
    e.target.style.height = "1px";
    e.target.style.height = e.target.scrollHeight + "px";
  }

  return (
    <div class="position-relative">
      {previewLogo ? (
        <img
          class="rounded-circle"
          src={previewLogo}
          width="200px"
          height="200px"
        />
      ) : (
        <img
          class="rounded-circle"
          src={company.comp_logo}
          width="200px"
          height="200px"
        />
      )}

      {isDisabled == "true" ? (
        <button class="btn btn-primary" onClick={handleEditCompClick}>
          Edit
        </button>
      ) : (
        <div>
          <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
          <input
            type="file"
            id="comp_logo"
            name="comp_logo"
            enctype="multipart/form-data"
            onChange={handleLogoPreview}
          />
        </div>
      )}

      <form method="post" onSubmit={handleCompanySubmit}>
        <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
        <div class="form-group">
          <label for="comp_name">Company Name</label>
          <input
            type="text"
            class="form-control"
            id="comp_name"
            name="comp_name"
            disabled={isDisabled == "true" ? true : false}
            placeholder="Company Name"
            value={company.comp_name}
            onChange={handleCompanyChange}
            required
          />
        </div>
        <div class="form-group">
          <label for="comp_name">Company Thai Name</label>
          <input
            type="text"
            class="form-control"
            id="comp_name_th"
            name="comp_name_th"
            disabled={isDisabled == "true" ? true : false}
            placeholder="Company Thai Name"
            value={company.comp_name_th}
            onChange={handleCompanyChange}
          />
        </div>
        <div class="form-group">
          <label for="comp_name">Company Desciption</label>
          <textarea
            type="text"
            class="form-control"
            id="comp_desc"
            name="comp_desc"
            disabled={isDisabled == "true" ? true : false}
            placeholder="Company Desciption"
            value={company.comp_desc}
            onChange={handleCompanyChange}
            onKeyUp={textAreaAdjust}
          ></textarea>
        </div>
        <div class="form-group">
          <label for="comp_name">Company Address</label>
          <textarea
            type="text"
            class="form-control"
            id="comp_address"
            name="comp_address"
            disabled={isDisabled == "true" ? true : false}
            placeholder="Company Address"
            value={company.comp_address}
            onChange={handleCompanyChange}
            onKeyUp={textAreaAdjust}
            required
          ></textarea>
        </div>
        <div class="form-group">
          <label for="comp_name">Company Contact Info</label>
          <textarea
            type="text"
            class="form-control"
            id="comp_contact_info"
            name="comp_contact_info"
            disabled={isDisabled == "true" ? true : false}
            placeholder="Company Contact Info"
            value={company.comp_contact_info}
            onChange={handleCompanyChange}
            onKeyUp={textAreaAdjust}
            required
          ></textarea>
        </div>
        {isDisabled == "false" && (
          <div>
            <input
              class="btn btn-primary"
              type="submit"
              value="Submit"
              onClick={handleLogoUpload}
            />
            <button class="btn btn-primary" onClick={handleCancleCompClick}>
              Cancle
            </button>
          </div>
        )}
        <Map lat={Number(company.comp_lat)} long={Number(company.comp_long)} />
      </form>
      {posts.map((post) => {
        return <PostSection post={post} />;
      })}
    </div>
  );
};

ReactDOM.render(<CompanyProfile />, document.querySelector("#company"));
