
interface Device {
  name: string;
  display_name: string;
  description: string;
  state: any;
  updated_at: Date;
}

export const isValidDevice = (device: any): boolean => {
  return (
    typeof device?.name === "string" &&
    typeof device?.display_name === "string" &&
    typeof device?.description === "string" &&
    device?.state !== undefined
  );
};

export default Device;
