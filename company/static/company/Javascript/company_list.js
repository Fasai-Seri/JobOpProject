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
        <input
          id="search"
          class="form-control"
          type="search"
          placeholder="Search.."
          name="search_term"
        />
      </form>
    );
  }

  function Company(props) {
    return (
      <div class="border rounded">
        <img
          class="rounded-circle"
          src={props.comp.comp_logo}
          width="200px"
          height="200px"
        />
        <p>
          <a href={comp_href + "/" + props.comp.comp_id}>
            {props.comp.comp_name}
          </a>
        </p>
        <p>{props.comp.comp_desc}</p>
      </div>
    );
  }
  return (
    <div>
      <SearchBar />
      {isEmployer == "True" && (
        <a class="btn btn-primary" href={create_comp_link}>
          Create Company
        </a>
      )}
      {companies.length == 0 ? (
        <h2>No company found</h2>
      ) : (
        companies.map((comp) => {
          return <Company comp={comp} />;
        })
      )}
    </div>
  );
};

ReactDOM.render(<CompanyList />, document.querySelector("#company_list"));
