
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
    next("/");
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
