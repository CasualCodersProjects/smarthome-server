import type { NextApiRequest, NextApiResponse } from 'next';
import { MongoClient } from 'mongodb';
import Device, { isValidDevice } from '@/types/device';
import { formatISO } from 'date-fns';

const mongo = new MongoClient('mongodb://localhost:27017');

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // Allow only POST, PUT, and OPTIONS requests
  if (!['POST', 'PUT', 'OPTIONS'].includes(req.method as string)) {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // If the request method is OPTIONS, return a 204 status code
  if (req.method === 'OPTIONS') {
    return res.status(204).end();
  }

  // Check if the request body is in the same format as Device
  if (!isValidDevice(req.body)) {
    return res.status(400).json({ error: 'Invalid device format' });
  }

  // Get the device from the request body
  const device: Device = req.body;

  // Use the default database "default" and the collection "devices"
  const db = mongo.db('default');
  const collection = db.collection<Device>('devices');
  const query = { name: device.name };

  if (!device.updated_at) {
    // If the device doesn't have an updated_at field, add it
    device.updated_at = new Date();
  }

  // Upsert the device: if the device is not present, add it to the DB, otherwise, update it
  await collection.updateOne(query, { $set: device }, { upsert: true });

  // Return the updated or inserted device with a 200 status code
  return res.status(200).json(device);
}
