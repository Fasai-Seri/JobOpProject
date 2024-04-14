const CreateCompany = () => {
  const [previewLogo, setPreviewLogo] = React.useState("");
  const data = document.getElementById("create_company_script").dataset;
  const csrftoken = data.csrfToken;

  function handlePreviewLogo() {
    const logo = document.querySelector("#comp_logo").files[0];
    setPreviewLogo(URL.createObjectURL(logo));
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
      <form id="comp_form" method="post" enctype="multipart/form-data">
        <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
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
          Company Name: <input class="form-control" name="comp_name" required />
        </div>
        <div class="form-group">
          Company Thai Name: <input class="form-control" name="comp_name_th" />
        </div>
        <div class="form-group">
          Company Description:{" "}
          <textarea class="form-control" name="comp_desc"></textarea>
        </div>
        <div class="form-group">
          Company Address:{" "}
          <textarea
            class="form-control"
            name="comp_address"
            required
          ></textarea>
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
      </form>
    </div>
  );
};

ReactDOM.render(<CreateCompany />, document.querySelector("#create_company"));
