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
  const can_edit = data.canEdit;

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

  async function handleFavPost(post_id) {
    await fetch(`favorite/${post_id}`, {
      method: "POST",
      headers: { "X-CSRFToken": csrftoken },
    });
    fetch_company_posts();
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

  async function handleFollowClick() {
    await fetch(`follow_company/${comp_id}`);
    fetch_company();
  }

  function PostSection(props) {
    console.log(props);
    return (
      <div class="mt-3">
        <div class="card mb-3">
          <div class="row no-gutters align-items-center">
            <div class="col-md-2">
              <div class="d-flex align-items-center justify-content-center">
                <img
                  src={props.post.company_logo}
                  class="rounded-circle"
                  width="100px"
                  height="100px"
                />
              </div>
            </div>
            <div class="col-md-10">
              <div class="card-body">
                <h5 class="job_title card-title">{props.post.job_title}</h5>
                <h6>
                  <a
                    class="company card-subtitle mb-3 text-muted"
                    href={data.compHref.slice(0, -1) + "/" + props.post.comp_id}
                  >
                    {props.post.company}
                  </a>
                </h6>

                <div class="job_type card-text">
                  {props.post.job_type.charAt(0).toUpperCase() +
                    props.post.job_type.slice(1)}
                </div>
                <div class="job_type card-text">{props.post.job_location}</div>
                <div class="d-flex align-items-center mt-3">
                  <div
                    class="status-badge mr-2 rounded-circle"
                    id={
                      props.post.job_status == "active"
                        ? "show_active"
                        : "show_inactive"
                    }
                  ></div>

                  <div class="job_status card-text">
                    {props.post.job_status == "active" ? "Active" : "Inactive"}
                  </div>
                </div>
                <hr />
                <a
                  href={post_href + "/" + props.post.job_id}
                  style={{ color: "black" }}
                >
                  <button class="btn btn-outline-dark mt-2">Read More</button>
                </a>
                {props.post.isFavorite ? (
                  <div
                    type="button"
                    class="favorite-button"
                    onClick={() => handleFavPost(props.post.job_id)}
                  >
                    <div
                      class="position-absolute"
                      style={{ top: "20px", right: "20px" }}
                    >
                      <img
                        width="40vh"
                        height="40vh"
                        src="https://icons.iconarchive.com/icons/designbolts/free-valentine-heart/256/Heart-icon.png"
                      />
                    </div>
                  </div>
                ) : (
                  <div
                    type="button"
                    class="favorite-button"
                    onClick={() => handleFavPost(props.post.job_id)}
                  >
                    <div
                      class="position-absolute"
                      style={{ top: "20px", right: "20px" }}
                    >
                      <img
                        width="40vh"
                        height="40vh"
                        src="https://cdn-icons-png.freepik.com/256/1077/1077035.png"
                      />
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
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
      if (props.disabled == "false") {
        map.current.addControl(gc, "top-left");
      }

      map.current.on("click", async function (e) {
        if (props.disabled == "false") {
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
            "Marked Location:" + String(results.features[0].place_name_en);

          compAdd.current = {
            comp_long: e.lngLat.lng,
            comp_lat: e.lngLat.lat,
            comp_address: results.features[0].place_name_en,
          };
          console.log(company);
          console.log(compAdd);
        }
      });
    }, [API_KEY, center, zoom]);

    return (
      <div>
        <div class="form-group">
          <label for="comp_name">
            <b>Company Address</b>
          </label>
          <textarea
            type="text"
            class="form-control"
            id="comp_address"
            name="comp_address"
            disabled
            value={company.comp_address}
            required
          ></textarea>
        </div>
        <div id="info" class="position-relative d-block p-2 mt-2 rounded"></div>
        <div ref={mapContainer} class="position-absolute w-100 h-50" />
      </div>
    );
  }

  function textAreaAdjust(e) {
    e.target.style.height = "1px";
    e.target.style.height = e.target.scrollHeight + "px";
  }

  $(".custom-file-input, .logo").on("change", function () {
    console.log("triggered");
    const file = $(this).val();
    const fileName = file.split("\\")[file.split("\\").length - 1];
    $(this).next(".custom-file-label, .logo").html(fileName);
  });

  return (
    <div class="container mt-3">
      <div class="row justify-content-center">
        <div class="col-md-12">
          <div class="mb-3 bg-light p-4 rounded shadow-sm">
            {isDisabled == "true" && can_edit == "True" && (
              <button
                class="btn btn-outline-dark float-right"
                onClick={handleEditCompClick}
              >
                Edit
              </button>
            )}
            {isDisabled == "true" && (
              <button
                class="btn btn-dark float-right mr-2"
                onClick={handleFollowClick}
              >
                <input
                  type="hidden"
                  name="csrfmiddlewaretoken"
                  value={csrftoken}
                />
                {company.isFollowedByUser ? "Unfollow" : "follow"}
              </button>
            )}
            <h4>Company Profile</h4>
            <hr />

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
              <div></div>
            ) : (
              <div>
                <input
                  type="hidden"
                  name="csrfmiddlewaretoken"
                  value={csrftoken}
                />
                <div class="custom-file">
                  <input
                    type="file"
                    class="custom-file-input logo"
                    id="comp_logo"
                    name="comp_logo"
                    onChange={handleLogoPreview}
                  />
                  <label
                    class="custom-file-label logo"
                    for="comp_logo"
                    id="file_label"
                  >
                    Choose file
                  </label>
                </div>
              </div>
            )}

            <form method="post" onSubmit={handleCompanySubmit}>
              <input
                type="hidden"
                name="csrfmiddlewaretoken"
                value={csrftoken}
              />
              <div class="form-group">
                <label for="comp_name">
                  <b>Company Name</b>
                </label>
                <input
                  type="text"
                  class="form-control"
                  id="comp_name"
                  name="comp_name"
                  disabled={isDisabled == "true" ? true : false}
                  value={company.comp_name}
                  onChange={handleCompanyChange}
                  required
                />
              </div>
              <div class="form-group">
                <label for="comp_name">
                  <b>Company Thai Name</b>
                </label>
                <input
                  type="text"
                  class="form-control"
                  id="comp_name_th"
                  name="comp_name_th"
                  disabled={isDisabled == "true" ? true : false}
                  value={company.comp_name_th}
                  onChange={handleCompanyChange}
                />
              </div>
              <div class="form-group">
                <label for="comp_name">
                  <b>Company Description</b>
                </label>
                <textarea
                  type="text"
                  class="form-control"
                  id="comp_desc"
                  name="comp_desc"
                  disabled={isDisabled == "true" ? true : false}
                  value={company.comp_desc}
                  onChange={handleCompanyChange}
                  onKeyUp={textAreaAdjust}
                ></textarea>
              </div>
              <div class="form-group">
                <label for="comp_name">
                  <b>Company Contact Info</b>
                </label>
                <textarea
                  type="text"
                  class="form-control"
                  id="comp_contact_info"
                  name="comp_contact_info"
                  disabled={isDisabled == "true" ? true : false}
                  value={company.comp_contact_info}
                  onChange={handleCompanyChange}
                  onKeyUp={textAreaAdjust}
                  required
                ></textarea>
              </div>

              <div
                style={{ height: isDisabled == "true" ? "1600px" : "1400px" }}
              >
                <Map
                  lat={Number(company.comp_lat)}
                  long={Number(company.comp_long)}
                  disabled={isDisabled}
                />
              </div>
              {isDisabled == "false" && (
                <div>
                  <input
                    class="btn btn-dark mr-2"
                    type="submit"
                    value="Submit"
                    onClick={handleLogoUpload}
                  />
                  <button
                    class="btn btn-outline-dark"
                    onClick={handleCancleCompClick}
                  >
                    Cancle
                  </button>
                </div>
              )}
            </form>
            {isDisabled == "true" && (
              <div>
                <h3 class="mt-3">Posts</h3>
                <hr />
                {posts.length > 0 ? (
                  <div>
                    {posts.map((post) => {
                      console.log(post);
                      return <PostSection post={post} />;
                    })}
                  </div>
                ) : (
                  <div>No post from this company</div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

ReactDOM.render(<CompanyProfile />, document.querySelector("#company"));
