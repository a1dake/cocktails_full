const API_URLS = {
  users: {
    info: "api/users/info/",
    updateInfo: "api/users/update_info/",
  },
  tables: {
    commonInfo: "api/table/",
    download: "api/export-csv/",
  },
  system: {
    all: "api/systems/",
    byID: "api/systems/$id/",
    update: "api/system-update/$id/",
    practice: "api/system-practice/?system_id=$id",
    changes: "api/systems-changes/",
  },
  triggers: {
    updateSystemStatus: "api/systems/$id/update-status/",
  },
  settings: "api/settings/",
  links: "api/links/",
  auth: "api/admin/auth/sign-in/",
};

export default API_URLS;
