const CreateCompany = () => {
  const [comp, setComp] = React.useState({});
  const [previewLogo, setPreviewLogo] = React.useState("");
  const data = document.getElementById("create_company_script").dataset;
  const csrftoken = data.csrfToken;

  function handlePreviewLogo() {
    const logo = document.querySelector("#comp_logo").files[0];
    setPreviewLogo(URL.createObjectURL(logo));
  }

  function handleCompChange(e) {
    const { name, value } = e.target;
    setComp((prevComp) => ({
      ...prevComp,
      [name]: value,
    }));
    console.log(name, value);
  }

  function handleCompSubmit() {
    const logo = document.querySelector("#comp_logo").files[0];
    const formData = new FormData();
    formData.append("comp_name", comp.comp_name);
    formData.append("comp_desc", comp.comp_desc);
    if (logo) {
      formData.append("comp_logo", logo);
    }
    fetch("create_company", {
      method: "POST",
      body: formData,
    });
  }

  return (
    <div>
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
      <div>
        <input
          type="file"
          class="form-control-file"
          id="comp_logo"
          name="comp_logo"
          enctype="multipart/form-data"
          onChange={handlePreviewLogo}
        />
      </div>
      <form id="comp_form" method="post" onSubmit={handleCompSubmit}>
        <input
          type="hidden"
          name="csrfmiddlewaretoken"
          value={csrftoken}
          onChange={handleCompChange}
        />
        <div class="form-group">
          Company Name:{" "}
          <input
            class="form-control"
            name="comp_name"
            onChange={handleCompChange}
          />
        </div>
        <div class="form-group">
          Company Description:{" "}
          <textarea
            class="form-control"
            name="comp_desc"
            onChange={handleCompChange}
          ></textarea>
        </div>
        <input type="submit" class="btn btn-primary" value="Create" />
      </form>
    </div>
  );
};

ReactDOM.render(<CreateCompany />, document.querySelector("#create_company"));
