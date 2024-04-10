const ProfilePanel = (props) => {
  const [user, setUser] = React.useState({});
  const [majors, setMajors] = React.useState([]);
  const [isDisabled, setIsDisabled] = React.useState("true");
  const data = document.getElementById("profile_script").dataset;
  const user_id = parseInt(data.userId, 10);
  const csrftoken = data.csrfToken;

  React.useEffect(() => {
    fetchUser();
    fetchMajors();
  }, []);

  React.useEffect(() => {}, [isDisabled]);

  function fetchUser() {
    fetch(`get_user/${user_id}`)
      .then((response) => response.json())
      .then((user) => {
        setUser(user);
        console.log(user);
      });
  }

  function fetchMajors() {
    fetch(`get_major`)
      .then((response) => response.json())
      .then((majors) => {
        console.log(majors);
        setMajors(majors);
      });
  }

  function handleEditClick() {
    setIsDisabled("false");
  }
  function handleCancleClick() {
    fetchUser();
    setIsDisabled("true");
  }

  function handleProfileChange(e) {
    const { name, value } = e.target;
    setUser((prevUser) => ({
      ...prevUser,
      [name]: value,
    }));
    console.log(name, value);
  }

  function handleProfileSubmit(e) {
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
  console.log(isDisabled);

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

  return (
    <div>
      {user.user_photo ? (
        <img src={user.user_photo} width="200" height="200" />
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
      {isDisabled == "true" && (
        <button class="btn btn-primary" onClick={handleEditClick}>
          Edit
        </button>
      )}
      <form id="profile_form" method="post" onSubmit={handleProfileSubmit}>
        <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
        {isDisabled == "True" && (
          <div class="form-group">
            <input
              type="file"
              class="form-control-file"
              id="profile_photo"
              name="user_photo"
              enctype="multipart/form-data"
              onChange={handleProfileChange}
            />
          </div>
        )}
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
          />
        </div>
        {user.type == "student" ? (
          <div>
            <MajorSelect />
            {isDisabled == "True" && (
              <div class="form-group">
                <label for="resume">Example file input</label>
                <input
                  type="file"
                  class="form-control-file"
                  id="resume"
                  name="resume"
                  onChange={handleProfileChange}
                />
              </div>
            )}
          </div>
        ) : user.type == "professor" ? (
          <MajorSelect />
        ) : (
          <div>
            <div class="form-group">Company</div>
            <div class="form-group">
              <label for="email">Position</label>
              <input
                type="text"
                class="form-control"
                id="position"
                name="position"
                placeholder="Position"
                disabled={isDisabled == "true" ? true : false}
                value={user.position}
                onChange={handleProfileChange}
              />
            </div>
          </div>
        )}

        <div class="form-group">
          <label for="exampleFormControlTextarea1">Example textarea</label>
          <textarea
            class="form-control"
            id="exampleFormControlTextarea1"
            rows="3"
          ></textarea>
        </div>
        {isDisabled == "false" && (
          <div>
            <input class="btn btn-primary" type="submit" value="Save" />
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
