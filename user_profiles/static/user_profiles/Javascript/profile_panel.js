const ProfilePanel = (props) => {
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
        >
          {majors.map((major) => (
            <option value={major.id}>
              {major.desc} ({major.id})
            </option>
          ))}
        </select>
      </div>
    );
  }

  $(document).ready(function () {
    $(".js-example-basic-single").select2();
  });

  $("#comp").on("change", function (e) {
    handleProfileChange(e);
  });

  return (
    <div>
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
          <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
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
      {isDisabled == "true" && user.user_id == current_user_id && (
        <button class="btn btn-primary" onClick={handleEditClick}>
          Edit
        </button>
      )}
      <form id="profile_form" method="post" onSubmit={handleProfileSubmit}>
        <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />

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
                <embed src={user.resume} width="50%" height="1050px" />:
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
            </div>
          )
        ) : user.type == "professor" ? (
          <MajorSelect />
        ) : (
          user.type == "employer" && (
            <div>
              <div class="form-group">Company</div>
              <select
                class="js-example-basic-single js-states form-control"
                id="comp"
                name="comp"
                disabled={isDisabled == "true" ? true : false}
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
              class="btn btn-primary"
              onClick={() => {
                handleUploadProfile();
                handleUploadResume();
              }}
              type="submit"
              value="Save"
            />
            <button class="btn btn-primary" onClick={handleCancleClick}>
              Cancle
            </button>
          </div>
        )}
      </form>
    </div>
  );
};

ReactDOM.render(<ProfilePanel />, document.querySelector("#profile"));
