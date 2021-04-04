// get all the stars
const one = document.getElementById('first')
const two = document.getElementById('second')
const three = document.getElementById('third')
const four = document.getElementById('fourth')
const five = document.getElementById('fifth')

//const avgrating = document.getElementsByClassName('avgrating')
const avgrating = document.getElementById('avgrating').innerHTML
document.getElementById("hidden").style.cssText = "font-size: 0.01px; color: black; "


const stars = document.querySelector('.stars')
const form = document.querySelector('.rate-form')
const confirmBox = document.getElementById('confirm-box')
const csrf = document.getElementsByName('csrfmiddlewaretoken')


const handleStarSelect = (size, place) => {
	const children = place.children
	
	for (let i=0; i < children.length; i++) {
		if (i <= size) {
			children[i].classList.add('checked')
		} else {
			children[i].classList.remove('checked')
		}
	}
}



switch(avgrating) {
	case '1': {
		handleStarSelect(0, stars)
		break
	}
	case '2': {
		handleStarSelect(1, stars)
		break
	}
	case '3': {
		handleStarSelect(2, stars)
		break
	}
	case '4': {
		handleStarSelect(3, stars)
		break
	}
	case '5': {
		handleStarSelect(4, stars)
		break
	}
}
	
	
	
const handleSelect = (selection) => {
	switch(selection){
		case 'first': {
			//one.classList.add('checked')
			//two.classList.remove('checked')
			//three.classList.remove('checked')
			//four.classList.remove('checked')
			//five.classList.remove('checked')
			handleStarSelect(1, form)
			return
		}
		case 'second': {
			handleStarSelect(2, form)
			return
		}
		case 'third': {
			handleStarSelect(3, form)
			return
		}
		case 'fourth': {
			handleStarSelect(4, form)
			return
		}
		case 'fifth': {
			handleStarSelect(5, form)
			return
		}
	}
}


const getNumericValue = (stringValue) => {
	let numericValue;
	if (stringValue == 'first') {
		numericValue = 1
	}
	else if (stringValue == 'second') {
		numericValue = 2
	}
	else if (stringValue == 'third') {
		numericValue = 3
	}
	else if (stringValue == 'fourth') {
		numericValue = 4
	}
	else if (stringValue == 'fifth') {
		numericValue = 5
	}
	else {
		numericValue = 0
	}
	return numericValue
	
}



if (one) {
	const arr = [one, two, three, four, five]
	
	arr.forEach(item=> item.addEventListener('mouseover', (event)=>{
		handleSelect(event.target.id)
	}))
	
	arr.forEach(item => item.addEventListener('click', (event) => {
		const val = event.target.id
		
		let isSubmit = false
		
		form.addEventListener('submit', e => {
			e.preventDefault()
			
			if (isSubmit) {
				return
			}
			isSubmit = true
			
			const val_num = getNumericValue(val)
			
			
			$.ajax({
				type: 'POST',
				url: '/ratemyrecipe/rate/',
				data: {
					'csrfmiddlewaretoken': csrf[0].value,
					'val': val_num,
				},
				processData: false,
				contentType: false,
				success: function(response) {
					
					console.log(response)
					confirmBox.outerHTML = `<h1>Successfully rated</h1>`
				},
				error: function(error) {
					console.log(error)

					confirmBox.outerHTML = `<h1>Oops... something went wrong</h1>`
				}
			})
		})
	}))
}

