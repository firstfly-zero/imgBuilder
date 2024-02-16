export type RoleType = '' | '*' | 'admin' | 'user' | 'userVip0' | 'userVip1' | 'userVip2' | 'userVip3';
export interface UserState {
  name?: string;
  avatar?: string;
  email?: string;
  inviter?: string;
  inviteNum?: number;
  albumList?: [
    {
      album_name?: string,
      desc?: string,
      cover?: string,
      image_num?: number
    }
  ];
  role: RoleType;
  job?: string;
  organization?: string;
  location?: string;
  introduction?: string;
  personalWebsite?: string;
  jobName?: string;
  organizationName?: string;
  locationName?: string;
  phone?: string;
  registrationDate?: string;
  accountId?: string;
  certification?: number;
  galleryId?: string;
}
