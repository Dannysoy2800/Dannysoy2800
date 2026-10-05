# सुरक्षित फ़ाइल ऑर्गनाइज़र

`personal-ai-os organize <path>` किसी डायरेक्टरी की केवल सीधे मौजूद, non-hidden
regular files का विश्लेषण करता है। यह सुझाव पहले देता है; डिफ़ॉल्ट रूप से कोई
फ़ाइल move, rename, overwrite, या delete नहीं होती।

```bash
personal-ai-os organize ~/Downloads
```

सुझाव फ़ाइल extension के आधार पर `Documents`, `Images`, `Archives`, `Source`,
`Audio`, `Video`, या `Other` श्रेणियों में दिखते हैं। प्रत्येक परिणाम में एक
deterministic confidence score और playful “scientific experiment” संदेश होता है।

## सुझाव लागू करना

सुझाव review करने के बाद ही `--apply` का उपयोग करें:

```bash
personal-ai-os organize ~/Downloads --apply
```

यह केवल उसी command से बने सुझावों को लागू करता है। यदि destination में उसी नाम
की फ़ाइल पहले से मौजूद है, तो organizer सुरक्षित नया नाम चुनता है, जैसे
`report (2).pdf`; मौजूदा फ़ाइल कभी overwrite नहीं होती।
