const CompanyProfile = () => {
  const [company, setCompany] = React.useState({});
  const [isDisabled, setIsDiabled] = React.useState("true");
  const [previewLogo, setPreviewLogo] = React.useState("");
  const data = document.getElementById("company_script").dataset;
  const comp_id = parseInt(data.compId, 10);
  const csrftoken = data.csrfToken;
  console.log(csrftoken);
  React.useEffect(() => {
    fetch_company();
  }, []);

  console.log(company);

  function fetch_company() {
    fetch(`get_company/${comp_id}`)
      .then((response) => response.json())
      .then((comp) => {
        setCompany(comp);
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
    console.log(name, value);
  }

  function handleCompanySubmit() {
    fetch(`update_company/${comp_id}`, {
      method: "POST",
      body: JSON.stringify({
        comp_name: company.comp_name,
        comp_name_th: company.comp_name_th,
        comp_desc: company.comp_desc,
        comp_address: company.comp_address,
        comp_contact_info: company.comp_contact_info,
      }),
    });
    console.log(company);
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

  function textAreaAdjust(e) {
    e.target.style.height = "1px";
    e.target.style.height = e.target.scrollHeight + "px";
  }

  return (
    <div>
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
      </form>
    </div>
  );
};

ReactDOM.render(<CompanyProfile />, document.querySelector("#company"));
