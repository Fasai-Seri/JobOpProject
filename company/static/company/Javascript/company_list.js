const CompanyList = () => {
  const data = document.querySelector("#company_list_script").dataset;
  const companies = JSON.parse(data.companies);
  const csrftoken = data.csrfToken;
  const isEmployer = data.isEmployer;
  const create_comp_link = data.createComp;
  const comp_href = data.compHref.slice(0, -1);
  console.log(comp_href);

  function SearchBar() {
    return (
      <form method="GET">
        <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
        <div class="d-flex">
          <input
            id="search"
            class="form-control"
            type="search"
            placeholder="Search.."
            name="search_term"
          />
          <span class="input-group-btn ml-2">
            <button class="btn btn-dark" type="submit">
              <i class="fa fa-search"></i>
            </button>
          </span>
        </div>
      </form>
    );
  }

  function Company(props) {
    return (
      <div class="mt-3">
        <div class="card mb-3">
          <div class="row no-gutters align-items-center">
            <div class="col-md-2 m-2">
              <div class="d-flex align-items-center justify-content-center">
                <img
                  class="rounded-circle"
                  src={props.comp.comp_logo}
                  width="150vw"
                  height="150vh"
                />
              </div>
            </div>
            <div class="card-body">
              <h5 class="job_title card-title">
                <a href={comp_href + "/" + props.comp.comp_id}>
                  {props.comp.comp_name}
                </a>
              </h5>
              <p>{props.comp.comp_desc}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }
  return (
    <div class="container mt-3">
      <div class="row justify-content-center">
        <div class="col-md-12">
          <div class="mb-3 bg-light p-4 rounded shadow-sm">
            {isEmployer == "True" && (
              <a class="btn btn-dark float-right" href={create_comp_link}>
                Create Company
              </a>
            )}
            <h4>Company List</h4>
            <hr />
            <SearchBar />
            {companies.length == 0 ? (
              <h2>No company found</h2>
            ) : (
              companies.map((comp) => {
                return <Company comp={comp} />;
              })
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

ReactDOM.render(<CompanyList />, document.querySelector("#company_list"));
