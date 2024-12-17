const mongoose = require('mongoose');

const SupplierSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true,
  },
  contactPerson: {
    type: String,
    required: true,
    trim: true,
  },
  phoneNumber: {
    type: String,
    required: true,
  },
  businessType: {
    type: String,
    required: true,
  },
  taxID: {
    type: String,
    required: true,
    unique: true,
  },
  address: {
    type: String,
    required: true,
  },
  description: {
    type: String,
  },
  parameters: {
    annualturnover: {
      type: Number,
    },
    controllocation: {
      type: String,
    },
    inhousedesigncapability: {
      type: Boolean,
    },
    isocertified: {
      type: Boolean,
    },
    hsepolicy: {
      type: Boolean,
    },
    qaqcpolicy: {
      type: Boolean,
    },
    factorylocation: {
      type: String,
    },
    distancefromgurgaon: {
      type: Number,
    },
    unitperdaycapacity: {
      type: Number,
    },
    maxshifts: {
      type: Number,
    },
    panelproductioncapacityperday: {
      type: Number,
    },
    inhousemsfabrication: {
      type: Boolean,
    },
    inhousepowdercoatingcapability: {
      type: Boolean,
    },
    opentobidwithmultiplesystems: {
      type: Boolean,
    },
    bidusingownsystem: {
      type: Boolean,
    },
    engineeringstaffcapacity: {
      type: Number,
    },
    pastsimilarprojects: {
      type: String,
    },
    productioncapacity: {
      type: Number,
    },
    installationcapacity: {
      type: Number,
    },
    averagerating: {
      type: Number,
    },
    recommended: {
      type: Boolean,
    }
  },
  
});

const Supplier = mongoose.model('Supplier', SupplierSchema);

module.exports = Supplier;
