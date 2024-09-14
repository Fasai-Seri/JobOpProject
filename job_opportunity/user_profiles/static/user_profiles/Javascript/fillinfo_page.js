const FillInfo = () => {
  const [majors, setMajors] = React.useState([]);
  React.useEffect(() => {
    fetchMajors();
  }, []);

  function fetchMajors() {
    fetch(`get_major`)
      .then((response) => response.json())
      .then((majors) => {
        setMajors(majors);
      });
  }

  function handleMajorChange(e) {
  }

  function MajorSelect() {
    return (
      <div class="form-group">
        <label for="major">Major</label>
        <select
          class="form-control"
          id="major"
          name="major"
          onChange={handleMajorChange}
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
  return <MajorSelect />;
};

ReactDOM.render(<FillInfo />, document.querySelector("#majorselect"));
