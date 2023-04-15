// pages/api/all.ts
import type { NextApiRequest, NextApiResponse } from 'next';
import { MongoClient } from 'mongodb';
import type Device from '@/types/device';

const mongo = new MongoClient('mongodb://localhost:27017');

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  // allow only GET and OPTIONS requests
  if (!['GET', 'OPTIONS'].includes(req.method as string)) {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  // if the request method is OPTIONS, return a 204 status code
  if (req.method === 'OPTIONS') {
    return res.status(204).end()
  }

  // Use the default database "default" and the collection "devices"
  const db = mongo.db('default');
  const collection = db.collection<Device>('devices');

  // Get all devices from the collection
  const devices = await collection.find().toArray();

  // Return the devices with a 200 status code
  return res.status(200).json(devices);
}
