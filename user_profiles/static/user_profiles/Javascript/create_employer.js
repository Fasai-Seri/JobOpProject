const CreateEmployer = () => {
  //   const [emp, setEmp] = React.useState({});
  //   const data = document.getElementById("create_employer_script").dataset;
  //   const csrftoken = data.csrfToken;
  //   function handleEmpChange(e) {
  //     const { name, value } = e.target;
  //     setEmp((prevEmp) => ({
  //       ...prevEmp,
  //       [name]: value,
  //     }));
  //     console.log(name, value);
  //   }
  //   function handleEmpSubmit() {
  //     fetch("", {
  //       method: "POST",
  //       body: JSON.stringify({
  //         email: emp.email,
  //         password: emp.password,
  //       }),
  //     });
  //   }
  //   return (
  //     <div>
  //       <form id="create_emp_form" method="post">
  //         <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
  //         <div class="form-group">
  //           <input
  //             type="email"
  //             class="form-control"
  //             name="email"
  //             placeholder="foo@exmaple.com"
  //             onChange={handleEmpChange}
  //           />
  //         </div>
  //         <div class="form-group">
  //           <input
  //             class="form-control"
  //             type="password"
  //             name="password"
  //             placeholder="Password"
  //             onChange={handleEmpChange}
  //           />
  //         </div>
  //         <div class="form-group">
  //           <input
  //             class="form-control"
  //             type="password"
  //             name="confirmation"
  //             placeholder="Confirm Password"
  //             onChange={handleEmpChange}
  //           />
  //         </div>
  //         <input
  //           class="btn btn-primary"
  //           type="submit"
  //           value="Create Employer Account"
  //         />
  //       </form>
  //     </div>
  //   );
};

ReactDOM.render(<CreateEmployer />, document.querySelector("#create_employer"));
