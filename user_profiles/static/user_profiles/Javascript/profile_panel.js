const ProfilePanel = () => {
  const [user, setUser] = React.useState({});
  const [majors, setMajors] = React.useState([]);
  const [isDisabled, setIsDisabled] = React.useState("true");
  const [previewPhoto, setPreviewPhoto] = React.useState("");
  const [previewResume, setPreviewResume] = React.useState("");
  const [companies, setCompanies] = React.useState([]);
  const [isNewEmp, setIsNewEmp] = React.useState(false);
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
        if (user.comp == "") {
          setIsNewEmp(true);
        }
      });
  }

  function fetchMajors() {
    fetch(`get_major`)
      .then((response) => response.json())
      .then((majors) => {
        setMajors(majors);
      });
  }

  function fetchCompanies() {
    fetch("get_company")
      .then((response) => response.json())
      .then((companies) => {
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
  }

  function handlePreviewProfile() {
    const photo = document.querySelector("#profile_photo").files[0];
    setPreviewPhoto(URL.createObjectURL(photo));
  }
  function handlePreviewResume() {
    const resume = document.querySelector("#resume").files[0];
    setPreviewResume(URL.createObjectURL(resume));
  }

  function handleUploadResume() {
    if (user.type == "student") {
      const resume = document.querySelector("#resume").files[0];
      if (resume) {
        const formData = new FormData();
        formData.append("student_resume", resume);

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

  async function handleProfileSubmit() {
    const formData = new FormData();
    const photo = document.querySelector("#profile_photo").files[0];
    formData.append("fname", user.fname);
    formData.append("lname", user.lname);
    formData.append("phone", user.phone);
    formData.append("user_photo", photo ? photo : user.user_photo);
    if (user.type == "employer") {
      formData.append("comp", user.comp);
      formData.append("emp_position", user.emp_position == null ? '' : user.emp_position);
      fetch(`update_user`, {
        method: "POST",
        body: formData,
      });
    } else {
      formData.append("major", user.major);
      fetch(`update_user`, {
        method: "POST",
        body: formData,
      });
    }
  }

  function MajorSelect() {
    return (
      <div class="form-group">
        <label for="major">
          <b>Major</b>
        </label>
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
      if (isDisabled == "false") {
        return (
          <div>
            <h5 class="mt-3">Portfolio</h5>
            <hr />

            <input
              type="file"
              class="form-control"
              id="portfolio"
              name="portfolio"
              multiple
            />
            <p class="mt-3">Current Files</p>
            {user.student_portfolio.map((file) => {
              const file_name = String(file.student_portfolio).split("/")[
                String(file.student_portfolio).split("/").length - 1
              ];
              return (
                <div>
                  <input
                    type="button"
                    class="btn btn-dark mr-2 mt-2 mb-2"
                    onClick={() => handleButtonClick(file.student_portfolio)}
                    value={file_name}
                  />

                  <input
                    type="button"
                    class="btn btn-outline-dark mt-2"
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
              height="500px"
            />
          </div>
        );
      } else {
        return (
          <div>
            <h5 class="mt-3">Portfolio</h5>
            <hr />
            <div>
            {user.student_portfolio.map((file) => {
              const file_name = String(file.student_portfolio).split("/")[
                String(file.student_portfolio).split("/").length - 1
              ];
              return (
                <input
                  type="button"
                  class="btn btn-dark mr-2 mt-2 mb-2"
                  onClick={() => handleButtonClick(file.student_portfolio)}
                  value={file_name}
                />
              );
            })}
            </div>  
            <embed
              id="portfolio_display"
              src={user.student_portfolio[0].student_portfolio}
              width="50%"
              height="500px"
            />
          </div>
        );
      }
    } else {
      if (isDisabled == "true") {
        return (
          <div>
            <h5>Portfolio</h5>
            <hr />
            <div class="mb-3">
              <p class="text-muted">No Portfolio</p>
            </div>
          </div>
        );
      } else {
        return (
          <div>
            <h5>Portfolio</h5>
            <hr />
            <div class="mb-3">
              <input
                type="file"
                class="form-control"
                id="portfolio"
                name="portfolio"
                multiple
              />
            </div>
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

  $(".custom-file-input, .photo").on("change", function () {
    const file = $(this).val();
    const fileName = file.split("\\")[file.split("\\").length - 1];
    $(this).next(".custom-file-label, .photo").html(fileName);
  });
  $(".custom-file-input, .resume").on("change", function () {
    const file = $(this).val();
    const fileName = file.split("\\")[file.split("\\").length - 1];
    $(this).next(".custom-file-label, .resume").html(fileName);
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
                <div class="custom-file mt-3">
                  <input
                    type="file"
                    class="custom-file-input photo"
                    id="profile_photo"
                    name="user_photo"
                    enctype="multipart/form-data"
                    onChange={handlePreviewProfile}
                  />
                  <label
                    class="custom-file-label photo"
                    for="profile_photo"
                    id="file_label"
                  >
                    Choose Profile Image
                  </label>
                </div>
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
                <label for="fname">
                  <b>First Name</b>
                </label>
                <input
                  type="text"
                  class="form-control"
                  id="fname"
                  name="fname"
                  disabled={isDisabled == "true" ? true : false}
                  value={user.fname}
                  onChange={handleProfileChange}
                  required
                  minlength="3"
                />
              </div>
              <div class="form-group">
                <label for="lname">
                  <b>Last name</b>
                </label>
                <input
                  type="text"
                  class="form-control"
                  id="lname"
                  name="lname"
                  disabled={isDisabled == "true" ? true : false}
                  value={user.lname}
                  onChange={handleProfileChange}
                  required
                  minlength="3"
                />
              </div>
              <div class="form-group">
                <label for="phone">
                  <b>Phone number</b>
                </label>
                <input
                  type="text"
                  class="form-control"
                  id="phone"
                  name="phone"
                  disabled={isDisabled == "true" ? true : false}
                  value={user.phone}
                  onChange={handleProfileChange}
                  required
                  minlength="10"
                  maxlength="10"
                />
              </div>
              <div class="form-group">
                <label for="email">
                  <b>Email address</b>
                </label>
                <input
                  type="email"
                  class="form-control"
                  id="email"
                  name="email"
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
                      <h5>Resume</h5>
                      <hr />
                      <embed src={user.resume} width="50%" height="500px" />
                      <StudentPortfolio />
                    </div>
                  ) : previewResume ? (
                    <div>
                      <MajorSelect />
                      <h5>Resume</h5>
                      <hr />
                      <div class="custom-file">
                        <input
                          type="file"
                          class="custom-file-input resume"
                          id="resume"
                          name="resume"
                          onChange={handlePreviewResume}
                        />
                        <label
                          class="custom-file-label resume"
                          for="portfolio"
                          id="file_label"
                        >
                          Choose file
                        </label>
                      </div>

                      <embed src={previewResume} width="50%" height="500px" />
                      <StudentPortfolio />
                    </div>
                  ) : (
                    <div>
                      <MajorSelect />
                      <h5>Resume</h5>
                      <hr />
                      <div class="custom-file">
                        <input
                          type="file"
                          class="custom-file-input resume"
                          id="resume"
                          name="resume"
                          onChange={handlePreviewResume}
                        />
                        <label
                          class="custom-file-label resume"
                          for="portfolio"
                          id="file_label"
                        >
                          Choose file
                        </label>
                      </div>
                      <embed src={user.resume} width="50%" height="500px" />
                      <StudentPortfolio />
                    </div>
                  )
                ) : isDisabled == "true" ? (
                  <div>
                    <MajorSelect />
                    <h5>Resume</h5>
                    <hr />
                    <p class="text-muted">No Resume</p>
                    <StudentPortfolio />
                  </div>
                ) : previewResume ? (
                  <div>
                    <MajorSelect />
                    <h5>Resume</h5>
                    <hr />
                    <div class="custom-file">
                      <input
                        type="file"
                        class="custom-file-input resume"
                        id="resume"
                        name="resume"
                        onChange={handlePreviewResume}
                      />
                      <label
                        class="custom-file-label resume"
                        for="portfolio"
                        id="file_label"
                      >
                        Choose file
                      </label>
                    </div>
                    <embed src={previewResume} width="50%" height="500px" />
                    <StudentPortfolio />
                  </div>
                ) : (
                  <div>
                    <MajorSelect />
                    <h5>Resume</h5>
                    <hr />
                    <div class="custom-file">
                      <input
                        type="file"
                        class="custom-file-input resume"
                        id="resume"
                        name="resume"
                        onChange={handlePreviewResume}
                      />
                      <label
                        class="custom-file-label resume"
                        for="portfolio"
                        id="file_label"
                      >
                        Choose file
                      </label>
                    </div>
                    <StudentPortfolio />
                  </div>
                )
              ) : user.type == "professor" ? (
                <MajorSelect />
              ) : (
                user.type == "employer" && (
                  <div>
                    <div class="form-group">
                      <b>Company</b>
                    </div>
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
                        isDisabled == "true" ? true : isNewEmp ? false : true
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
                      <label for="email">
                        <b>Position</b>
                      </label>
                      <input
                        type="text"
                        class="form-control"
                        id="emp_position"
                        name="emp_position"
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
                    class="btn btn-dark mr-2"
                    onClick={() => {
                      handleUploadResume();
                      handleUploadPortfolio();
                    }}
                    type="submit"
                    value="Save"
                  />
                  <button
                    class="btn btn-outline-dark"
                    onClick={handleCancleClick}
                  >
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
