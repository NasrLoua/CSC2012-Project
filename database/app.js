const express = require('express')
const { getDb, connectToDb } = require('./db')
const { ObjectId } = require('mongodb')

const app = express()
app.use(express.json())

let db

connectToDb((err) => {
    if (!err) {
        app.listen(3010, () => {
            console.log('app listening on port 3010')
        })
        db = getDb()
    }
})



app.get('/users', (req, res) => {
    let userArray = []
    
    db.collection('Users')
        .find()
        .sort({ name: 1 })
        .forEach(element => userArray.push(element))
        .then(() => {
            res.status(200).json(userArray)
        })
        .catch(() => {
            res.status(500).json({error: 'Could not fetch documents'})
        })

})

app.get('/users/:id', (req, res) => {

    if (ObjectId.isValid(req.params.id)) {
  
      db.collection('Users')
        .findOne({_id: new ObjectId(req.params.id)})
        .then(doc => {
          res.status(200).json(doc)
        })
        .catch(err => {
          res.status(500).json({error: 'Could not fetch the document'})
        })
        
    } else {
      res.status(500).json({error: 'Could not fetch the document'})
    }
  
  })

  app.post('/users', (req, res) => {
    const book = req.body
  
    db.collection('Users')
      .insertOne(book)
      .then(result => {
        res.status(201).json(result)
      })
      .catch(err => {
        res.status(500).json({err: 'Could not create new document'})
      })
  })

  app.delete('/users/:id', (req, res) => {

    if (ObjectId.isValid(req.params.id)) {
  
    db.collection('Users')
      .deleteOne({ _id: new ObjectId(req.params.id) })
      .then(result => {
        res.status(200).json(result)
      })
      .catch(err => {
        res.status(500).json({error: 'Could not delete document'})
      })
  
    } else {
      res.status(500).json({error: 'Could not delete document'})
    }
  })

  app.patch('/users/:id', (req, res) => {
    const updates = req.body
  
    if (ObjectId.isValid(req.params.id)) {
  
      db.collection('Users')
        .updateOne({ _id: new ObjectId(req.params.id) }, {$set: updates})
        .then(result => {
          res.status(200).json(result)
        })
        .catch(err => {
          res.status(500).json({error: 'Could not update document'})
        })
  
    } else {
      res.status(500).json({error: 'Could not update document'})
    }
  })