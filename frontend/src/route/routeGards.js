/*
 * Copyright (C) 2020-2024 LIG Université Grenoble Alpes
 *
 *
 * This file is part of Matos.
 *
 * FacManager is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
 *
 * Matos is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along with FacManager. If not, see <https://www.gnu.org/licenses/>
 *
 * @author Germain Lemasson
 * @author Clément Lesaulnier
 * @author Robin Courault
*/

import { useAuthStore } from "@/stores/auth";

export async function requireAuth(to, from, next) {
  const store = useAuthStore();
  if (!store.isAuthenticated) {
    await store.checkAuth();
  }
  if (store.isAuthenticated) {
    if (
      to.name == "profile" ||
      (store.authUser.first_name &&
        store.authUser.last_name &&
        store.authUser.email &&
        store.authUser.rgpd_accept)
    ) {
      next();
    } else {
      next({
        name: "profile",
      });
    }
  } else {
    window.location.href=import.meta.env.VITE_APP_LOGIN_URL;
  }
}
export async function requireAdmin(to, from, next) {
  const store = useAuthStore();
  if (!store.isAuthenticated) {
    await store.checkAuth();
  }
  if (store.isAuthenticated && store.isAdmin) {
    next();
  } else {
    next({
      name: "home",
    });
  }
}
export function requireManager(to, from, next) {
  const store = useAuthStore();
  if (store.isAuthenticated) {
    var user = store.authUser;
    if (
      user.entities.indexOf(parseInt(to.params["entityid"])) > -1 ||
      store.isAdmin
    ) {
      next();
    } else {
      next("/");
    }
  }
}
