const ProfilePanel = () => {
  const [user, setUser] = React.useState({});
  const [majors, setMajors] = React.useState([]);
  const [isDisabled, setIsDisabled] = React.useState("true");
  const [previewPhoto, setPreviewPhoto] = React.useState("");
  const [previewResume, setPreviewResume] = React.useState("");
  const [companies, setCompanies] = React.useState([]);
  const data = document.getElementById("profile_script").dataset;
  const user_id = parseInt(data.userId, 10);
  const current_user_id = parseInt(data.currentUserId, 10);
  const csrftoken = data.csrfToken;
  const create_comp = data.createComp;

  React.useEffect(() => {
    fetchUser();
    fetchMajors();
    fetchCompanies();
  }, []);

  function fetchUser() {
    fetch(`get_user/${user_id}`)
      .then((response) => response.json())
      .then((user) => {
        setUser(user);
        console.log(user);
      });
  }
  console.log(user);

  function fetchMajors() {
    fetch(`get_major`)
      .then((response) => response.json())
      .then((majors) => {
        console.log(majors);
        setMajors(majors);
      });
  }

  function fetchCompanies() {
    fetch("get_company")
      .then((response) => response.json())
      .then((companies) => {
        console.log(companies);
        setCompanies(companies);
      });
  }

  function handleEditClick() {
    setIsDisabled("false");
  }
  function handleCancleClick() {
    fetchUser();
    setIsDisabled("true");
    setPreviewPhoto("");
    setPreviewResume("");
    $("#comp").val(`${user.comp}`).trigger("change");
  }

  function handleProfileChange(e) {
    const { name, value } = e.target;
    setUser((prevUser) => ({
      ...prevUser,
      [name]: value,
    }));
    console.log(name, value);
  }

  function handlePreviewProfile() {
    const photo = document.querySelector("#profile_photo").files[0];
    setPreviewPhoto(URL.createObjectURL(photo));
  }
  function handlePreviewResume() {
    const resume = document.querySelector("#resume").files[0];
    setPreviewResume(URL.createObjectURL(resume));
  }

  function handleUploadProfile() {
    const photo = document.querySelector("#profile_photo").files[0];
    if (photo) {
      const formData = new FormData();
      formData.append("user_photo", photo);
      console.log(photo);
      fetch("update_user_photo", {
        method: "POST",
        body: formData,
      });
    }
  }

  function handleUploadResume() {
    if (user.type == "student") {
      const resume = document.querySelector("#resume").files[0];
      if (resume) {
        const formData = new FormData();
        formData.append("student_resume", resume);
        console.log(resume);
        fetch("update_student_resume", {
          method: "POST",
          body: formData,
        });
      }
    }
  }

  function handleUploadPortfolio() {
    if (user.type == "student") {
      const portfolio = document.querySelector("#portfolio").files;
      console.log(portfolio);
      if (portfolio) {
        const formData = new FormData();
        for (let i = 0; i < portfolio.length; i++) {
          formData.append("student_portfolio", portfolio[i], portfolio[i].name);
        }
        fetch("update_student_portfolio", {
          method: "POST",
          body: formData,
        });
      }
    }
  }

  async function handleRemovePortfolio(file_name) {
    await fetch(`remove_student_portfolio/${file_name}`);
    fetchUser();
  }

  function handleProfileSubmit() {
    if (user.type == "employer") {
      fetch(`update_user`, {
        method: "POST",
        body: JSON.stringify({
          fname: user.fname,
          lname: user.lname,
          phone: user.phone,
          user_photo: user.user_photo,
          comp: user.comp,
          emp_position: user.emp_position,
        }),
      });
    } else {
      fetch(`update_user`, {
        method: "POST",
        body: JSON.stringify({
          fname: user.fname,
          lname: user.lname,
          phone: user.phone,
          major: user.major,
          user_photo: user.user_photo,
        }),
      });
    }
  }

  function MajorSelect() {
    return (
      <div class="form-group">
        <label for="major">Major</label>
        <select
          class="form-control"
          id="major"
          value={user.major}
          name="major"
          disabled={isDisabled == "true" ? true : false}
          onChange={handleProfileChange}
          required
        >
          <option></option>
          {majors.map((major) => (
            <option value={major.id}>
              {major.desc} ({major.id})
            </option>
          ))}
        </select>
      </div>
    );
  }

  function StudentPortfolio() {
    function handleButtonClick(file) {
      const display = document.getElementById("portfolio_display");
      const clone = display.cloneNode(true);
      clone.setAttribute("src", file);
      display.parentNode.replaceChild(clone, display);
    }

    if (user.student_portfolio) {
      if (isDisabled == "true") {
        return (
          <div>
            <p>Portfolio</p>
            {user.student_portfolio.map((file) => {
              const file_name = String(file.student_portfolio).split("/")[
                String(file.student_portfolio).split("/").length - 1
              ];
              return (
                <div>
                  <input
                    type="button"
                    onClick={() => handleButtonClick(file.student_portfolio)}
                    value={file_name}
                  />
                  <input
                    type="button"
                    onClick={() => handleRemovePortfolio(file_name)}
                    value="Remove"
                  />
                </div>
              );
            })}
            <embed
              id="portfolio_display"
              src={user.student_portfolio[0].student_portfolio}
              width="50%"
              height="1050px"
            />
          </div>
        );
      } else {
        return (
          <div>
            <p>Portfolio</p>
            <input
              type="file"
              class="form-control-file"
              id="portfolio"
              name="portfolio"
              multiple
            />
            {user.student_portfolio.map((file) => {
              const file_name = String(file.student_portfolio).split("/")[
                String(file.student_portfolio).split("/").length - 1
              ];
              return (
                <input
                  type="button"
                  onClick={() => handleButtonClick(file.student_portfolio)}
                  value={file_name}
                />
              );
            })}
            <embed
              id="portfolio_display"
              src={user.student_portfolio[0].student_portfolio}
              width="50%"
              height="1050px"
            />
          </div>
        );
      }
    } else {
      if (isDisabled == "true") {
        return (
          <div>
            <p>Portfolio</p>

            <input
              type="text"
              class="form-control"
              disabled
              value="No Portfolio"
            />
          </div>
        );
      } else {
        return (
          <div>
            <p>Portfolio</p>
            <input
              type="file"
              class="form-control-file"
              id="portfolio"
              name="portfolio"
              multiple
            />
            ;
          </div>
        );
      }
    }
  }

  $(document).ready(function () {
    $("#comp").select2({
      placeholder: "Select your company",
      allowClear: true,
    });
  });

  $("#comp").on("change", function (e) {
    handleProfileChange(e);
  });

  return (
    <div class="container mt-3">
      <div class="row justify-content-center">
        <div class="col-md-7">
          <div class="mb-3 bg-light p-4 rounded shadow-sm">
            {isDisabled == "true" && user.user_id == current_user_id && (
              <div>
                <button
                  class="btn btn-dark float-right"
                  onClick={handleEditClick}
                >
                  Edit
                </button>
              </div>
            )}
            <h4>User Profiles</h4>
            <hr />

            {previewPhoto ? (
              <img
                class="rounded-circle"
                src={previewPhoto}
                width="200"
                height="200"
              />
            ) : user.user_photo ? (
              <img
                class="rounded-circle"
                src={user.user_photo}
                width="200"
                height="200"
              />
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="200"
                height="200"
                fill="currentColor"
                class="bi bi-person-circle"
                viewBox="0 0 16 16"
              >
                <path d="M11 6a3 3 0 1 1-6 0 3 3 0 0 1 6 0" />
                <path
                  fill-rule="evenodd"
                  d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8m8-7a7 7 0 0 0-5.468 11.37C3.242 11.226 4.805 10 8 10s4.757 1.225 5.468 2.37A7 7 0 0 0 8 1"
                />
              </svg>
            )}
            {isDisabled == "false" && (
              <div>
                <input
                  type="hidden"
                  name="csrfmiddlewaretoken"
                  value={csrftoken}
                />
                <input
                  type="file"
                  class="form-control-file"
                  id="profile_photo"
                  name="user_photo"
                  enctype="multipart/form-data"
                  onChange={handlePreviewProfile}
                />
              </div>
            )}

            <form
              id="profile_form"
              method="post"
              onSubmit={handleProfileSubmit}
            >
              <input
                type="hidden"
                name="csrfmiddlewaretoken"
                value={csrftoken}
              />

              <div class="form-group">
                <label for="fname">First name</label>
                <input
                  type="text"
                  class="form-control"
                  id="fname"
                  name="fname"
                  placeholder="First name"
                  disabled={isDisabled == "true" ? true : false}
                  value={user.fname}
                  onChange={handleProfileChange}
                  required
                  minlength="3"
                />
              </div>
              <div class="form-group">
                <label for="lname">Last name</label>
                <input
                  type="text"
                  class="form-control"
                  id="lname"
                  name="lname"
                  placeholder="Last name"
                  disabled={isDisabled == "true" ? true : false}
                  value={user.lname}
                  onChange={handleProfileChange}
                  required
                  minlength="3"
                />
              </div>
              <div class="form-group">
                <label for="phone">Phone number</label>
                <input
                  type="text"
                  class="form-control"
                  id="phone"
                  name="phone"
                  placeholder="Phone number"
                  disabled={isDisabled == "true" ? true : false}
                  value={user.phone}
                  onChange={handleProfileChange}
                  required
                  minlength="10"
                  maxlength="10"
                />
              </div>
              <div class="form-group">
                <label for="email">Email address</label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  name="email"
                  placeholder="name@example.com"
                  disabled
                  value={user.email}
                  onChange={handleProfileChange}
                  required
                />
              </div>
              {user.type == "student" ? (
                user.resume ? (
                  isDisabled == "true" ? (
                    <div>
                      <MajorSelect />
                      <p>Resume</p>
                      <embed src={user.resume} width="50%" height="1050px" />
                      <StudentPortfolio />
                    </div>
                  ) : previewResume ? (
                    <div>
                      <MajorSelect />
                      <p>Resume</p>
                      <input
                        type="file"
                        class="form-control-file"
                        id="resume"
                        name="resume"
                        onChange={handlePreviewResume}
                      />
                      <embed src={previewResume} width="50%" height="1050px" />
                      <StudentPortfolio />
                    </div>
                  ) : (
                    <div>
                      <MajorSelect />
                      <p>Resume</p>
                      <input
                        type="file"
                        class="form-control-file"
                        id="resume"
                        name="resume"
                        onChange={handlePreviewResume}
                      />
                      <embed src={user.resume} width="50%" height="1050px" />
                      <StudentPortfolio />
                    </div>
                  )
                ) : isDisabled == "true" ? (
                  <div>
                    <MajorSelect />
                    <p>Resume</p>
                    <input
                      type="text"
                      class="form-control"
                      disabled
                      value="No Resume"
                    />
                    <StudentPortfolio />
                  </div>
                ) : previewResume ? (
                  <div>
                    <MajorSelect />
                    <p>Resume</p>
                    <input
                      type="file"
                      class="form-control-file"
                      id="resume"
                      name="resume"
                      onChange={handlePreviewResume}
                    />
                    <embed src={previewResume} width="50%" height="1050px" />
                    <StudentPortfolio />
                  </div>
                ) : (
                  <div>
                    <MajorSelect />
                    <p>Resume</p>
                    <input
                      type="file"
                      class="form-control-file"
                      id="resume"
                      name="resume"
                      onChange={handlePreviewResume}
                    />
                    <StudentPortfolio />
                  </div>
                )
              ) : user.type == "professor" ? (
                <MajorSelect />
              ) : (
                user.type == "employer" && (
                  <div>
                    <div class="form-group">Company</div>
                    <div hidden={user.comp ? true : false}>
                      <div>You can only edit this field once.</div>
                      <div>
                        Couldn't find your company?{" "}
                        <a href={create_comp}>Create Here</a>
                      </div>
                    </div>
                    <select
                      class="js-example-basic-single js-states form-control"
                      id="comp"
                      name="comp"
                      disabled={
                        user.comp ? true : isDisabled == "true" ? true : false
                      }
                      required
                    >
                      <option></option>
                      {companies.map((comp) => {
                        if (user.comp == comp.comp_id) {
                          return (
                            <option value={comp.comp_id} selected="selected">
                              {comp.comp_name}
                            </option>
                          );
                        } else {
                          return (
                            <option value={comp.comp_id} selected="">
                              {comp.comp_name}
                            </option>
                          );
                        }
                      })}
                    </select>
                    <div class="form-group">
                      <label for="email">Position</label>
                      <input
                        type="text"
                        class="form-control"
                        id="emp_position"
                        name="emp_position"
                        placeholder="Position"
                        value={user.emp_position}
                        disabled={isDisabled == "true" ? true : false}
                        onChange={handleProfileChange}
                      />
                    </div>
                  </div>
                )
              )}
              {isDisabled == "false" && (
                <div>
                  <input
                    class="btn btn-dark"
                    onClick={() => {
                      handleUploadProfile();
                      handleUploadResume();
                      handleUploadPortfolio();
                    }}
                    type="submit"
                    value="Save"
                  />
                  <button class="btn btn-dark" onClick={handleCancleClick}>
                    Cancle
                  </button>
                </div>
              )}
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

ReactDOM.render(<ProfilePanel />, document.querySelector("#profile"));
