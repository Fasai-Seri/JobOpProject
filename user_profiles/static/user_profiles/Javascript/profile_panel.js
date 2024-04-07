const ProfilePanel = (props) => {
  const [user, setUser] = React.useState([]);
  const [majors, setMajors] = React.useState([]);
  const data = document.getElementById("profile_script").dataset;
  const user_id = parseInt(data.userId, 10);

  React.useEffect(() => {
    fetchUser();
    fetchMajors();
  }, []);

  function fetchUser() {
    fetch(`get_user/${user_id}`)
      .then((response) => response.json())
      .then((user) => {
        setUser(user, () => {
          console.log(user);
        });
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

  return (
    <div>
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
      <form>
        <div class="form-group">
          <label for="fname">First name</label>
          <input
            type="text"
            class="form-control"
            id="fname"
            placeholder="First name"
            value={user.fname}
          />
        </div>
        <div class="form-group">
          <label for="lname">Last name</label>
          <input
            type="text"
            class="form-control"
            id="lname"
            placeholder="Last name"
            value={user.lname}
          />
        </div>
        <div class="form-group">
          <label for="phone">Phone number</label>
          <input
            type="text"
            class="form-control"
            id="phone"
            placeholder="Phone number"
            value={user.phone}
          />
        </div>
        <div class="form-group">
          <label for="exampleFormControlInput1">Email address</label>
          <input
            type="email"
            class="form-control"
            id="exampleFormControlInput1"
            placeholder="name@example.com"
            value={user.email}
          />
        </div>
        <div class="form-group">
          <label for="major">Major</label>
          <select class="form-control" id="major">
            {majors.map((major) => (
              <option>
                {major.desc} ({major.id})
              </option>
            ))}
          </select>
        </div>
        <div class="form-group">
          <label for="exampleFormControlSelect2">Example multiple select</label>
          <select multiple class="form-control" id="exampleFormControlSelect2">
            <option>1</option>
            <option>2</option>
            <option>3</option>
            <option>4</option>
            <option>5</option>
          </select>
        </div>
        <div class="form-group">
          <label for="exampleFormControlTextarea1">Example textarea</label>
          <textarea
            class="form-control"
            id="exampleFormControlTextarea1"
            rows="3"
          ></textarea>
        </div>
      </form>
    </div>
  );
};

ReactDOM.render(<ProfilePanel />, document.querySelector("#profile"));
