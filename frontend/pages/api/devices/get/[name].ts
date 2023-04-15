// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import type { NextApiRequest, NextApiResponse } from 'next'
import { MongoClient } from 'mongodb'
import type Device from '@/types/device'

const mongo = new MongoClient('mongodb://localhost:27017')

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  // allow only GET and OPTIONS requests
  if (!['GET', 'OPTIONS'].includes(req.method as string)) {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  // if the request method is OPTIONS, return a 204 status code
  if (req.method === 'OPTIONS') {
    return res.status(204).end()
  }

  const { name } = req.query;

  // get the device with the specific name from the database
  // use the default database "default" and the collection "devices"
  const db = mongo.db('default')
  const collection = db.collection<Device>('devices')
  const query = { name: name as string }
  const device = await collection.findOne(query)
  if (!device) {
    return res.status(404).json({ error: 'Device not found' })
  }

  // return the device
  return res.status(200).json(device)
}
