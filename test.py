import asyncio
import cv2
import numpy as np
from aiortc import RTCPeerConnection, RTCSessionDescription
from av import VideoFrame
import aiohttp

class VideoReceiver:
    def __init__(self):
        self.track = None
        self.running = True

    async def handle_track(self, track):
        print("Inside handle track")
        self.track = track
        while self.running:
            try:
                print("Waiting for frame...")
                frame = await asyncio.wait_for(track.recv(), timeout=5.0)
                
                if isinstance(frame, VideoFrame):
                    print(f"Frame type: VideoFrame, pts: {frame.pts}, time_base: {frame.time_base}")
                    frame = frame.to_ndarray(format="bgr24")
                elif isinstance(frame, np.ndarray):
                    print(f"Frame type: numpy array")
                else:
                    print(f"Unexpected frame type: {type(frame)}")
                    continue

                frame = cv2.resize(frame, (960, 540)) 
                cv2.imshow("Frame", frame)
    
                # Exit on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False
                    break
            except asyncio.TimeoutError:
                print("Timeout waiting for frame, continuing...")
            except Exception as e:
                print(f"Error in handle_track: {str(e)}")
                if "Connection" in str(e):
                    break
        
        cv2.destroyAllWindows()
        print("Exiting handle_track")

async def run(pc: RTCPeerConnection, camera_ip: str, stream_path: str, video_receiver: VideoReceiver):
    @pc.on("track")
    def on_track(track):
        print(f"Receiving {track.kind} track")
        asyncio.ensure_future(video_receiver.handle_track(track))

    @pc.on("datachannel")
    def on_datachannel(channel):
        print(f"Data channel established: {channel.label}")

    @pc.on("connectionstatechange")
    async def on_connectionstatechange():
        print(f"Connection state is {pc.connectionState}")
        if pc.connectionState == "connected":
            print("WebRTC connection established successfully")

    pc.addTransceiver("video", direction="recvonly")

    # Create offer
    print("Creating offer...")
    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    print("Local description set")

    # Send offer to camera via HTTP
    url = f"http://{camera_ip}{stream_path}"
    print(f"Sending offer to {url}")
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            url,
            headers={"Content-Type": "application/sdp"},
            data=offer.sdp
        ) as response:
            if response.status == 200:
                answer_data = await response.json()
                print("Received answer from camera")
                
                # Set remote description with the answer
                answer = RTCSessionDescription(sdp=answer_data["sdp"], type="answer")
                await pc.setRemoteDescription(answer)
                print("Remote description set")
            else:
                print(f"Error: HTTP {response.status}")
                return

    print("Waiting for connection to be established...")
    while pc.connectionState != "connected" and pc.connectionState != "failed":
        await asyncio.sleep(0.1)

    if pc.connectionState == "failed":
        print("Connection failed!")
        return

    print("Connection established, waiting for frames...")

    # Wait until user quits
    while video_receiver.running:
        await asyncio.sleep(0.1)

    print("Closing connection")

async def main():
    # Use the same camera IP and stream path as in your HTML
    camera_ip = "10.10.1.200:30080"
    stream_path = "/index/api/webrtc?app=live&stream=stream1&type=play"
    
    pc = RTCPeerConnection()
    
    video_receiver = VideoReceiver()

    try:
        await run(pc, camera_ip, stream_path, video_receiver)
    except Exception as e:
        print(f"Error in main: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print("Closing peer connection")
        video_receiver.running = False
        cv2.destroyAllWindows()
        await pc.close()

if __name__ == "__main__":
    asyncio.run(main())