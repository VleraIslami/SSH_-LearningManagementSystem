import { Children, Navigate } from "react";

import { useAuthStore } from "../store/auth";

const PrivateRoute = ({ children }) => {
  // Merrni direkt vlerën e isLoggedIn nga useAuthStore
  const loggedIn = useAuthStore((state) => state.isLoggedIn);

  // Kontrollo nëse përdoruesi është loguar, nëse po kthe komponenetin, nëse jo, navigo në login
  return loggedIn ? <>{children}</> : <Navigate to="/login/" />;
};

export default PrivateRoute;

//kur e bon naj modul psh studenDashbord mes privateRoute eshte secured edhe i duhet userit mu bo login per me u qas
//
