const CompanyProfile = () => {
  const [company, setCompany] = React.useState({});
  const [isDisabled, setIsDiabled] = React.useState("true");
  const data = document.getElementById("company_script").dataset;
  const comp_id = parseInt(data.compId, 10);
  React.useEffect(() => {
    fetch_company();
  }, []);

  function fetch_company() {
    fetch(`get_company/${comp_id}`)
      .then((response) => response.json())
      .then((comp) => {
        setCompany(comp);
      });
  }

  function handleEditCompClick() {
    setIsDiabled("false");
  }
  function handleCancleCompClick() {
    fetch_company();
    setIsDiabled("true");
  }

  console.log(company);

  return (
    <div>
      <img class="rounded-circle" src="static\company\Images\default.jpg" />

      {isDisabled == "true" && (
        <button class="btn btn-primary" onClick={handleEditCompClick}>
          Edit
        </button>
      )}
      <form>
        <div class="form-group">
          <label for="comp_name">Company Name</label>
          <input
            type="text"
            class="form-control"
            id="comp_name"
            disabled={isDisabled == "true" ? true : false}
            placeholder="Company Name"
            value={company.comp_name}
          />
        </div>
        <div class="form-group">
          <label for="comp_name">Company Desciption</label>
          <input
            type="text"
            class="form-control"
            id="comp_desc"
            disabled={isDisabled == "true" ? true : false}
            placeholder="Company Desciption"
            value={company.comp_desc}
          />
        </div>
        {isDisabled == "false" && (
          <div>
            <input class="btn btn-primary" type="submit" value="Submit" />
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
